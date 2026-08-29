import { createTileLayerComponent, LayerProps } from "@react-leaflet/core";

import L from "leaflet";

export interface BlendedTileLayerProps extends LayerProps {
  /** Base map tile URL template, e.g. "https://.../{z}/{x}/{y}{r}.png" */
  baseUrl: string;
  /** Overlay (e.g. hillshade) tile URL template, blended on top of the base tile. */
  overlayUrl: string;
  /** Optional labels overlay, drawn last with plain source-over compositing. */
  labelsUrl?: string;
  attribution?: string;
  /** Canvas globalCompositeOperation used to blend overlayUrl onto baseUrl. Default: "multiply". */
  blendMode?: GlobalCompositeOperation;
  /** CSS filter() string applied while drawing the base tile. Default: "none". */
  baseFilter?: string;
  /** CSS filter() string applied while drawing the overlay tile. Default: "none". */
  overlayFilter?: string;
  /** Opacity (0-1) applied while drawing the overlay tile. Default: 1.0. */
  overlayOpacity?: number;
  maxZoom?: number;
  /**
   * Highest zoom level the tile servers actually have imagery for. Past this,
   * tiles are requested at maxNativeZoom and scaled up, matching stock
   * L.TileLayer behaviour, instead of requesting zoom levels the server
   * doesn't have.
   */
  maxNativeZoom?: number;
  /**
   * Subdomains used to fill the {s} placeholder in URL templates, matching
   * L.TileLayer's `subdomains` option. Default: ["a", "b", "c"].
   */
  subdomains?: string[];
  /**
   * Sets img.crossOrigin before loading tile images. Only enable this if
   * your tile servers send CORS headers (Access-Control-Allow-Origin) —
   * otherwise every tile image will fail to load. Needed if you ever want
   * to read pixels back off the map canvas (e.g. exporting the map as an
   * image). Default: false (unset, matches previous behaviour).
   */
  crossOrigin?: boolean | string;
}

interface CanvasBlendLayerOptions extends L.GridLayerOptions {
  baseUrl: string;
  overlayUrl: string;
  labelsUrl?: string;
  blendMode: GlobalCompositeOperation;
  baseFilter: string;
  overlayFilter: string;
  overlayOpacity: number;
  subdomains: string[];
  crossOrigin: boolean | string | false;
  maxNativeZoom?: number;
}

/**
 * Loads an image, rejecting with a real Error (rather than an empty
 * rejection) so failures can be reported to Leaflet's DoneCallback and
 * surfaced as a `tileerror` event instead of silently looking like success.
 */
const loadImg = (
  url: string,
  crossOrigin: boolean | string | false
): Promise<HTMLImageElement> =>
  new Promise((resolve, reject) => {
    const img = new Image();
    if (crossOrigin === true) {
      img.crossOrigin = "anonymous";
    } else if (typeof crossOrigin === "string") {
      img.crossOrigin = crossOrigin;
    }
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(`Failed to load tile image: ${url}`));
    img.src = url;
  });

/**
 * Given a display zoom `z` and coordinates, plus an optional
 * maxNativeZoom, returns the tile coordinates/zoom that should actually be
 * requested from the server, and the scale factor by which the fetched
 * tile should be stretched to still cover this tile's screen area. This
 * mirrors what L.TileLayer does internally via `_getZoomForUrl` when
 * `maxNativeZoom` is set, which our custom `createTile` otherwise bypasses.
 */
const getNativeTileRequest = (
  coords: L.Coords,
  maxNativeZoom: number | undefined
): { x: number; y: number; z: number; scale: number } => {
  if (maxNativeZoom == null || coords.z <= maxNativeZoom) {
    return { x: coords.x, y: coords.y, z: coords.z, scale: 1 };
  }
  const zoomDelta = coords.z - maxNativeZoom;
  const scale = Math.pow(2, zoomDelta);
  return {
    x: Math.floor(coords.x / scale),
    y: Math.floor(coords.y / scale),
    z: maxNativeZoom,
    scale,
  };
};

class CanvasBlendLayer extends L.GridLayer {
  private opts: CanvasBlendLayerOptions;

  constructor(options: CanvasBlendLayerOptions) {
    super(options);
    this.opts = options;
  }

  createTile(coords: L.Coords, done: L.DoneCallback): HTMLElement {
    const tile = L.DomUtil.create("canvas", "leaflet-tile") as HTMLCanvasElement;
    const size = this.getTileSize();
    tile.width = size.x;
    tile.height = size.y;
    const ctx = tile.getContext("2d");

    // Cancellation: Leaflet recycles/removes tile elements while panning.
    // Without this, an in-flight image load for a pruned tile can finish
    // later and draw stale imagery onto whatever tile now occupies this
    // canvas element. `_removeTile` (overridden below) flips this flag.
    let cancelled = false;
    (tile as unknown as { _cancel: () => void })._cancel = () => {
      cancelled = true;
    };

    if (!ctx) {
      setTimeout(() => done(undefined, tile), 0);
      return tile;
    }

    const subdomains =
      this.opts.subdomains && this.opts.subdomains.length > 0
        ? this.opts.subdomains
        : ["a", "b", "c"];
    const s = subdomains[Math.abs(coords.x + coords.y) % subdomains.length];
    const r = L.Browser.retina ? "@2x" : "";

    const native = getNativeTileRequest(coords, this.opts.maxNativeZoom);
    const templateVars = { x: native.x, y: native.y, z: native.z, s, r };

    const bUrl = L.Util.template(this.opts.baseUrl, templateVars);
    const oUrl = L.Util.template(this.opts.overlayUrl, templateVars);
    const lUrl = this.opts.labelsUrl
      ? L.Util.template(this.opts.labelsUrl, templateVars)
      : null;

    const drawScaled = (img: HTMLImageElement) => {
      // When native.scale > 1 we fetched a lower-zoom tile and need to
      // stretch + crop it to cover just this tile's portion of the parent,
      // matching how L.TileLayer upsamples past maxNativeZoom.
      if (native.scale === 1) {
        ctx.drawImage(img, 0, 0, size.x, size.y);
        return;
      }
      const cropSize = size.x / native.scale;
      const offsetX = (coords.x % native.scale) * cropSize;
      const offsetY = (coords.y % native.scale) * cropSize;
      ctx.drawImage(
        img,
        offsetX,
        offsetY,
        cropSize,
        cropSize,
        0,
        0,
        size.x,
        size.y
      );
    };

    loadImg(bUrl, this.opts.crossOrigin)
      .then((baseImg) => {
        if (cancelled) return;

        // 1. Draw base map
        ctx.save();
        if (this.opts.baseFilter && this.opts.baseFilter !== "none") {
          ctx.filter = this.opts.baseFilter;
        }
        drawScaled(baseImg);
        ctx.restore();

        // 2. Blend overlay (e.g. hillshade) on top
        return loadImg(oUrl, this.opts.crossOrigin)
          .then((overlayImg) => {
            if (cancelled) return;
            ctx.save();
            ctx.globalCompositeOperation = this.opts.blendMode;
            ctx.globalAlpha = this.opts.overlayOpacity;
            if (this.opts.overlayFilter && this.opts.overlayFilter !== "none") {
              ctx.filter = this.opts.overlayFilter;
            }
            drawScaled(overlayImg);
            ctx.restore();
          })
          .catch(() => {
            // Overlay is best-effort: a failed hillshade tile shouldn't
            // block the base map from displaying.
          })
          .then(() => {
            // 3. Draw clean labels on top, if provided
            if (cancelled || !lUrl) return;
            return loadImg(lUrl, this.opts.crossOrigin)
              .then((labelsImg) => {
                if (cancelled) return;
                ctx.save();
                ctx.globalCompositeOperation = "source-over";
                ctx.globalAlpha = 1;
                drawScaled(labelsImg);
                ctx.restore();
              })
              .catch(() => {
                // Labels are best-effort too.
              });
          });
      })
      .then(() => {
        if (!cancelled) done(undefined, tile);
      })
      .catch((err) => {
        if (!cancelled) done(err, tile);
      });

    return tile;
  }
}

export const BlendedTileLayer = createTileLayerComponent<
  CanvasBlendLayer,
  BlendedTileLayerProps
>(
  function createBlendedTileLayer(props, context) {
    const instance = new CanvasBlendLayer({
      ...props,
      blendMode: props.blendMode ?? "multiply",
      baseFilter: props.baseFilter ?? "none",
      overlayFilter: props.overlayFilter ?? "none",
      overlayOpacity: props.overlayOpacity ?? 1.0,
      maxZoom: props.maxZoom ?? 19,
      maxNativeZoom: props.maxNativeZoom ?? 16,
      subdomains: props.subdomains ?? ["a", "b", "c"],
      crossOrigin: props.crossOrigin ?? false,
    });
    return { instance, context };
  },
  function updateBlendedTileLayer(instance, props, prevProps) {
    if (
      props.baseUrl !== prevProps.baseUrl ||
      props.overlayUrl !== prevProps.overlayUrl ||
      props.labelsUrl !== prevProps.labelsUrl ||
      props.attribution !== prevProps.attribution ||
      props.blendMode !== prevProps.blendMode ||
      props.baseFilter !== prevProps.baseFilter ||
      props.overlayFilter !== prevProps.overlayFilter ||
      props.overlayOpacity !== prevProps.overlayOpacity ||
      props.maxNativeZoom !== prevProps.maxNativeZoom ||
      props.subdomains !== prevProps.subdomains ||
      props.crossOrigin !== prevProps.crossOrigin
    ) {
      instance.redraw();
    }
  }
);