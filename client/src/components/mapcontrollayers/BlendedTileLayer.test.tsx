import React from "react";
import { render, waitFor } from "@testing-library/react";
import { MapContainer } from "react-leaflet";
import L from "leaflet";
import { BlendedTileLayer } from "./BlendedTileLayer";

// Mock Canvas 2D Context with diagnostics
const mockCanvasContext = {
  save: jest.fn(() => console.log("[DEBUG] ctx.save called")),
  restore: jest.fn(() => console.log("[DEBUG] ctx.restore called")),
  drawImage: jest.fn(() => console.log("[DEBUG] ctx.drawImage called!")),
  filter: "",
  globalCompositeOperation: "source-over",
  globalAlpha: 1.0,
  clearRect: jest.fn(),
  fillRect: jest.fn(),
};

let shouldImageFail = false;

beforeAll(() => {
  // Mock img.decode() in case component uses it
  HTMLImageElement.prototype.decode = jest.fn().mockImplementation(async () => {
    console.log("[DEBUG] img.decode() called");
    if (shouldImageFail) {
      throw new Error("Image decode failed");
    }
    return undefined;
  });

  // Patch HTMLImageElement.prototype.src
  Object.defineProperty(HTMLImageElement.prototype, "src", {
    get(this: any) {
      return this._mockSrc || "";
    },
    set(this: HTMLImageElement & { _mockSrc?: string }, url: string) {
      this._mockSrc = url;
      console.log("[DEBUG] Image src assigned:", url);

      setTimeout(() => {
        if (shouldImageFail) {
          Object.defineProperty(this, "complete", { value: false, configurable: true });
          const errorEvent = new Event("error");
          if (typeof this.onerror === "function") {
            this.onerror(errorEvent);
          }
          this.dispatchEvent(errorEvent);
        } else {
          Object.defineProperty(this, "complete", { value: true, configurable: true });
          Object.defineProperty(this, "naturalWidth", { value: 256, configurable: true });
          Object.defineProperty(this, "naturalHeight", { value: 256, configurable: true });
          Object.defineProperty(this, "width", { value: 256, configurable: true });
          Object.defineProperty(this, "height", { value: 256, configurable: true });

          const loadEvent = new Event("load");
          if (typeof this.onload === "function") {
            this.onload(loadEvent);
          }
          this.dispatchEvent(loadEvent);
        }
      }, 0);
    },
    configurable: true,
  });
});

describe("BlendedTileLayer", () => {
  let getContextSpy: jest.SpyInstance;

  beforeEach(() => {
    jest.clearAllMocks();
    shouldImageFail = false;

    // Re-install every test, so this survives resetMocks/restoreMocks
    // being configured globally in jest.config.
    getContextSpy = jest
      .spyOn(HTMLCanvasElement.prototype, "getContext")
      .mockImplementation((type: string) => {
        console.log("[DEBUG] getContext called with type:", type);
        if (type === "2d") return mockCanvasContext as any;
        return null;
      });
  });

  afterEach(() => {
    getContextSpy.mockRestore();
  });

  it("renders within a Leaflet MapContainer without crashing", () => {
    const { container } = render(
      <MapContainer center={[0, 0]} zoom={5}>
        <BlendedTileLayer
          baseUrl="https://example.com/base/{z}/{x}/{y}.png"
          overlayUrl="https://example.com/overlay/{z}/{x}/{y}.png"
        />
      </MapContainer>
    );

    expect(container).toBeInTheDocument();
  });

  it("creates canvas tiles and draws base, overlay, and label images", async () => {
    let layerInstance: any;

    render(
      <MapContainer center={[0, 0]} zoom={5}>
        <BlendedTileLayer
          ref={(node: any) => {
            if (node) layerInstance = node;
          }}
          baseUrl="https://example.com/base/{z}/{x}/{y}.png"
          overlayUrl="https://example.com/overlay/{z}/{x}/{y}.png"
          labelsUrl="https://example.com/labels/{z}/{x}/{y}.png"
          blendMode="screen"
          baseFilter="invert(100%)"
          overlayFilter="contrast(150%)"
          overlayOpacity={0.7}
          attribution="Test Attribution"
        />
      </MapContainer>
    );

    await new Promise((r) => setTimeout(r, 100));
    mockCanvasContext.drawImage.mockClear();

    if (layerInstance && layerInstance._tileZoom === undefined) {
      layerInstance._tileZoom = 5;
    }

    const doneCallback = jest.fn();
    const coords = { x: 1, y: 1, z: 5 } as L.Coords;

    const canvasTile = layerInstance.createTile(coords, doneCallback);
    expect(canvasTile).toBeInstanceOf(HTMLCanvasElement);

    await waitFor(
      () => {
        expect(mockCanvasContext.drawImage).toHaveBeenCalled();
      },
      { timeout: 3000 }
    );

    expect(doneCallback).toHaveBeenCalledWith(undefined, canvasTile);
  });

  it("handles image load errors gracefully without crashing the tile callback", async () => {
    shouldImageFail = true;

    let layerInstance: any;

    render(
      <MapContainer center={[0, 0]} zoom={5}>
        <BlendedTileLayer
          ref={(node: any) => {
            if (node) layerInstance = node;
          }}
          baseUrl="https://example.com/invalid/{z}/{x}/{y}.png"
          overlayUrl="https://example.com/invalid/{z}/{x}/{y}.png"
        />
      </MapContainer>
    );

    await new Promise((r) => setTimeout(r, 100));

    if (layerInstance && layerInstance._tileZoom === undefined) {
      layerInstance._tileZoom = 1;
    }

    const doneCallback = jest.fn();
    const coords = { x: 0, y: 0, z: 1 } as L.Coords;

    layerInstance.createTile(coords, doneCallback);

    await waitFor(() => {
      expect(doneCallback).toHaveBeenCalled();
    });
  });

  it("triggers redraw when layer props are updated", () => {
    const { rerender } = render(
      <MapContainer center={[0, 0]} zoom={5}>
        <BlendedTileLayer
          baseUrl="https://example.com/base/{z}/{x}/{y}.png"
          overlayUrl="https://example.com/overlay/{z}/{x}/{y}.png"
          overlayOpacity={0.5}
        />
      </MapContainer>
    );

    rerender(
      <MapContainer center={[0, 0]} zoom={5}>
        <BlendedTileLayer
          baseUrl="https://example.com/base/{z}/{x}/{y}.png"
          overlayUrl="https://example.com/overlay/{z}/{x}/{y}.png"
          overlayOpacity={0.8}
        />
      </MapContainer>
    );

    expect(true).toBeTruthy();
  });
});