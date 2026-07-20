import { Tgo as TgoModel } from "../../api/liberationApi";
import backend from "../../api/backend";
import {
  useClearTgoDestinationMutation,
  useOpenNewTgoPackageDialogMutation,
  useOpenTgoInfoDialogMutation,
  useSetTgoDestinationMutation,
} from "../../api/liberationApi";
import {
  selectHighlightEmitters,
  selectHoveredEmitter,
  setHoveredEmitter,
} from "../../api/mapSlice";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import SplitLines from "../splitlines/SplitLines";
import { MovementPath, MovementPathHandle } from "../controlpoints/MovementPath";
import { TgoTooltip, iconForTgo } from "./shared";
import { LatLng, Marker as LMarker, LatLngLiteral } from "leaflet";
import { memo, useCallback, useEffect, useMemo, useRef, useState } from "react";
import ReactDOMServer from "react-dom/server";
import { Marker, Tooltip } from "react-leaflet";

// Distance/destination tooltip text, mirroring the carrier marker
// (MobileControlPoint) so a ship drag reads the same way: the live
// nautical-mile distance plus the destination coordinates, or an
// out-of-range notice with how far the attempted move was.
function metersToNauticalMiles(meters: number): number {
  return meters * 0.000539957;
}

function formatLatLng(latLng: LatLng): string {
  // Use the absolute value: the hemisphere is already carried by the N/S and
  // E/W suffix, so a southern/western coordinate must not also keep its minus
  // sign (e.g. "32.50&deg;S", not "-32.50&deg;S").
  const lat = Math.abs(latLng.lat).toFixed(2);
  const lng = Math.abs(latLng.lng).toFixed(2);
  const ns = latLng.lat >= 0 ? "N" : "S";
  const ew = latLng.lng >= 0 ? "E" : "W";
  return `${lat}&deg;${ns} ${lng}&deg;${ew}`;
}

function destinationTooltipText(
  tgo: TgoModel,
  destinationish: LatLngLiteral,
  inRange: boolean
): string {
  const destination = new LatLng(destinationish.lat, destinationish.lng);
  const distance = metersToNauticalMiles(
    destination.distanceTo(tgo.position)
  ).toFixed(1);
  if (!inRange) {
    return `Out of range (${distance}nm away)`;
  }
  return `${tgo.name} moving ${distance}nm to ${formatLatLng(
    destination
  )} next turn`;
}

interface PrimaryMarkerProps {
  tgo: TgoModel;
}

/**
 * The primary (draggable) marker for a mobile TGO.
 *
 * When no destination is queued, the marker sits at the TGO's current
 * position and behaves like a normal TGO marker (click → info dialog,
 * right-click → new package dialog, emitter hover).
 *
 * When a destination is queued, the marker moves to the destination,
 * becomes semi-transparent, and right-click cancels travel.  The
 * secondary marker at the origin then handles normal interaction.
 *
 * The MovementPath is rendered as a sibling (outside <Marker>) so it
 * is always on the map layer rather than inside the marker popup layer.
 * A ref lets the drag handler update the path's endpoint without
 * triggering a React re-render (which would interrupt dragging).
 */
function PrimaryMarker(props: PrimaryMarkerProps) {
  const markerRef = useRef<LMarker | null>(null);
  const pathRef = useRef<MovementPathHandle | null>(null);

  // Stable icon reference. iconForTgo() builds a fresh leaflet Icon every call;
  // if a re-render happens mid-drag (the busy TGO event stream churns this
  // component while unrelated ships/SAMs update), react-leaflet would call
  // marker.setIcon() with the new ref and abort the in-progress drag. Memoize
  // on the sidc so the ref only changes when the symbol actually changes.
  // Intentionally keyed on sidc only: the icon must stay referentially stable
  // across drags so a re-render can't swap it mid-drag (see comment above).
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const icon = useMemo(() => iconForTgo(props.tgo), [props.tgo.sidc]);

  const [hasDestination, setHasDestination] = useState<boolean>(
    props.tgo.destination != null
  );
  const [position, setPosition] = useState<LatLngLiteral>(
    props.tgo.destination ? props.tgo.destination : props.tgo.position
  );

  const setDestination = useCallback((destination: LatLng) => {
    setPosition(destination);
    setHasDestination(true);
  }, []);

  const resetDestination = useCallback(() => {
    setPosition(props.tgo.position);
    setHasDestination(false);
  }, [props]);

  const [putDestination, { isLoading }] = useSetTgoDestinationMutation();
  const [cancelTravel] = useClearTgoDestinationMutation();

  const [openInfoDialog] = useOpenTgoInfoDialogMutation();
  const [openNewPackageDialog] = useOpenNewTgoPackageDialogMutation();
  const dispatch = useAppDispatch();
  // Raised above other icons while this emitter (or its ring) is hovered,
  // matching the static TGO marker's behavior (#750).
  const raised = useAppSelector(
    (state) =>
      selectHighlightEmitters(state) &&
      selectHoveredEmitter(state) === props.tgo.id
  );

  // Set the tooltip content imperatively against the empty <Tooltip/> rendered
  // below.  Rendering React children inside the Tooltip crashes on the
  // key-driven remount when a destination is queued: Leaflet mutates the
  // tooltip DOM during the drag, so React's removeChild then fails on the stale
  // portal node (DOMException NotFoundError, white-screens the client).  The
  // carrier marker (MobileControlPoint) avoids this the same way.  The drag
  // handler overrides this content live via setTooltipContent.
  useEffect(() => {
    markerRef.current?.setTooltipContent(
      props.tgo.destination
        ? destinationTooltipText(props.tgo, props.tgo.destination, true)
        : ReactDOMServer.renderToString(
            <>
              {`${props.tgo.name} (${props.tgo.control_point_name})`}
              <br />
              <SplitLines items={props.tgo.units} />
            </>
          )
    );
  });

  return (
    <>
      <Marker
        position={position}
        icon={icon}
        draggable={!isLoading}
        autoPan
        zIndexOffset={raised ? 10000 : 1000}
        // Opacity (and the right-click branch below) follow the backend
        // destination, not local drag state, exactly like the carrier marker.
        // A rejected (e.g. out-of-range) release leaves props.destination null,
        // so the marker returns fully opaque instead of leaving a translucent
        // "move-to" ghost on top of the origin.
        opacity={props.tgo.destination ? 0.5 : 1}
        ref={(ref) => {
          if (ref != null) {
            markerRef.current = ref;
          }
        }}
        eventHandlers={{
          click: () => {
            if (!hasDestination) {
              openInfoDialog({ tgoId: props.tgo.id });
            }
          },
          contextmenu: () => {
            if (props.tgo.destination) {
              cancelTravel({ tgoId: props.tgo.id }).then(() => {
                resetDestination();
              });
            } else {
              openNewPackageDialog({ tgoId: props.tgo.id });
            }
          },
          mouseover: () =>
            dispatch(setHoveredEmitter({ id: props.tgo.id, source: "emitter" })),
          mouseout: () => dispatch(setHoveredEmitter(null)),
          drag: (event) => {
            const dest = event.target.getLatLng() as LatLng;
            backend
              .get(
                `/tgos/${props.tgo.id}/destination-in-range?lat=${dest.lat}&lng=${dest.lng}`
              )
              .then((inRange) => {
                markerRef.current?.setTooltipContent(
                  destinationTooltipText(props.tgo, dest, inRange.data)
                );
              });
            pathRef.current?.setDestination(dest);
          },
          dragend: async (event) => {
            const previous = new LatLng(position.lat, position.lng);
            const dest = event.target.getLatLng() as LatLng;
            setDestination(dest);
            try {
              await putDestination({
                tgoId: props.tgo.id,
                body: { lat: dest.lat, lng: dest.lng },
              }).unwrap();
            } catch (error) {
              console.error("setTgoDestination failed", error);
              // Restore the backend's truth on a rejected move (e.g. out of
              // range): snap the marker back and only keep "has destination"
              // if the ship actually has one queued server-side. Using
              // setDestination here would leave hasDestination=true, stranding
              // a translucent ghost and suppressing the next click.
              setPosition(previous);
              setHasDestination(props.tgo.destination != null);
            }
          },
        }}
      >
        {/* Empty tooltip; content is set imperatively (idle: name/units via
            the useEffect above; live: distance via the drag handler).  React
            children here would crash on the destination-remount — see comment
            above. */}
        <Tooltip />
      </Marker>
      <MovementPath
        source={props.tgo.position}
        destination={position}
        ref={pathRef}
      />
    </>
  );
}

interface SecondaryMarkerProps {
  tgo: TgoModel;
  destination: LatLngLiteral | undefined;
}

/**
 * The secondary (origin) marker for a mobile TGO.  Only rendered when a
 * destination is queued.  Handles the normal click → info and
 * right-click → new package interactions as well as emitter hover, so
 * those behaviors remain reachable while the primary marker is off at
 * the destination.
 */
function SecondaryMarker(props: SecondaryMarkerProps) {
  const dispatch = useAppDispatch();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const icon = useMemo(() => iconForTgo(props.tgo), [props.tgo.sidc]);
  const [openInfoDialog] = useOpenTgoInfoDialogMutation();
  const [openNewPackageDialog] = useOpenNewTgoPackageDialogMutation();
  const raised = useAppSelector(
    (state) =>
      selectHighlightEmitters(state) &&
      selectHoveredEmitter(state) === props.tgo.id
  );

  if (!props.destination) {
    return <></>;
  }

  return (
    <Marker
      position={props.tgo.position}
      icon={icon}
      zIndexOffset={raised ? 10000 : 0}
      eventHandlers={{
        click: () => {
          openInfoDialog({ tgoId: props.tgo.id });
        },
        contextmenu: () => {
          openNewPackageDialog({ tgoId: props.tgo.id });
        },
        mouseover: () =>
          dispatch(setHoveredEmitter({ id: props.tgo.id, source: "emitter" })),
        mouseout: () => dispatch(setHoveredEmitter(null)),
      }}
    >
      <TgoTooltip tgo={props.tgo} />
    </Marker>
  );
}

interface MobileTgoProps {
  tgo: TgoModel;
}

// Memoized so that updates to OTHER tgos (the event stream churns the whole
// tgos slice, re-rendering TgosLayer and every marker) don't re-render — and
// thereby interrupt the drag of — this ship. Only re-renders when this tgo's
// own object reference changes (e.g. its destination was set/cleared). This is
// the key behavioral difference from the carrier marker, whose control-point
// slice is quiet on the campaign map and so never needed the guard.
function MobileTgo(props: MobileTgoProps) {
  return (
    <>
      <PrimaryMarker tgo={props.tgo} key={props.tgo.destination ? 0 : 1} />
      <SecondaryMarker tgo={props.tgo} destination={props.tgo.destination} />
    </>
  );
}

export default memo(MobileTgo);
