import { Flight } from "../../api/liberationApi";
import {
  useGetTacticalOverlayForFlightQuery,
  useSelectFlightMutation,
} from "../../api/liberationApi";
import WaypointMarker from "../waypointmarker";
import { Polyline as LPolyline } from "leaflet";
import { ReactElement, useEffect, useRef } from "react";
import { CircleMarker, Polygon, Polyline } from "react-leaflet";

const BLUE_PATH = "#0084ff";
const RED_PATH = "#c85050";
const SELECTED_PATH = "#ffff00";

interface FlightPlanProps {
  flight: Flight;
  selected: boolean;
  highlight?: boolean;
}

const pathColor = (props: FlightPlanProps) => {
  if (props.selected && props.highlight) {
    return SELECTED_PATH;
  } else if (props.flight.blue) {
    return BLUE_PATH;
  } else {
    return RED_PATH;
  }
};

function FlightPlanPath(props: FlightPlanProps) {
  const color = pathColor(props);
  const waypoints = props.flight.waypoints;
  const [selectFlight] = useSelectFlightMutation();

  const polylineRef = useRef<LPolyline | null>(null);

  // Flight paths should be drawn under everything else. There seems to be an
  // issue where `interactive: false` doesn't do as its told (there's nuance,
  // see the bug for details). It looks better if we draw the other elements on
  // top of the flight plans anyway, so just push the flight plan to the back.
  //
  // https://github.com/dcs-liberation/dcs_liberation/issues/3295
  //
  // It's not possible to z-index a polyline (and leaflet says it never will be,
  // because this is a limitation of SVG, not leaflet:
  // https://github.com/Leaflet/Leaflet/issues/185), so we need to use
  // bringToBack() to push the flight paths to the back of the drawing once
  // they've been added to the map. They'll still draw on top of the map, but
  // behind everything than was added before them. Anything added after always
  // goes on top.
  useEffect(() => {
    if (props.selected) {
        polylineRef.current?.bringToFront();
    }
    else {
        polylineRef.current?.bringToBack();
    }
  });

  if (waypoints == null) {
    return <></>;
  }
  const points = waypoints
    .filter((waypoint) => waypoint.include_in_path)
    .map((waypoint) => waypoint.position);

  // Only blue flight plans are interactive: hovering highlights the route in
  // yellow and clicking selects the owning package (and flight) in the Qt
  // sidebar via a round-trip through the server.
  const interactive = props.flight.blue;

  return (
    <Polyline
      positions={points}
      pathOptions={{ color: color, interactive: interactive }}
      ref={polylineRef}
      eventHandlers={
        interactive
          ? {
              mouseover: () => {
                polylineRef.current?.setStyle({ color: SELECTED_PATH });
                polylineRef.current?.bringToFront();
              },
              mouseout: () => {
                if (!props.selected) {
                  polylineRef.current?.setStyle({ color: color });
                  polylineRef.current?.bringToBack();
                }
              },
              click: () => {
                selectFlight({ flightId: props.flight.id });
              },
            }
          : undefined
      }
    />
  );
}

const WaypointMarkers = (props: FlightPlanProps) => {
  if (!props.selected || props.flight.waypoints == null) {
    return <></>;
  }

  var markers: ReactElement[] = [];
  props.flight.waypoints?.forEach((p, idx) => {
    if (p.should_mark) {
      markers.push(
        <WaypointMarker
          key={idx}
          number={idx}
          waypoint={p}
          flight={props.flight}
        />
      );
    }
  });

  return <>{markers}</>;
};

const ENGAGEMENT = "#ffff00"; // unchanged: existing engagement-zone yellow
const TARGET = "#ff5a5a"; // attack-target marker

interface TacticalOverlayProps {
  flight: Flight;
}

function TacticalOverlayLayer(props: TacticalOverlayProps) {
  const { data, error } = useGetTacticalOverlayForFlightQuery(
    { flightId: props.flight.id },
    // RTK Query can only invalidate caches from mutations, but this data is
    // invalidated by websocket events. Disable the cache and refetch on
    // (re)mount instead. It won't redraw until the component remounts; there
    // doesn't appear to be a better hook.
    { refetchOnMountOrArgChange: true }
  );
  if (error) {
    console.error(
      `Error loading tactical overlay for ${props.flight.id}`,
      error
    );
    return <></>;
  }
  if (!data) {
    return <></>;
  }
  const teamColor = props.flight.blue ? BLUE_PATH : RED_PATH;
  return (
    <>
      {data.reach.map((shape, idx) => (
        <Polygon
          key={`reach-${idx}`}
          positions={shape.polygon}
          pathOptions={
            shape.filled
              ? { color: ENGAGEMENT, weight: 1.5, fillOpacity: 0.15 }
              : { color: ENGAGEMENT, weight: 1.5, fill: false }
          }
          interactive={false}
        />
      ))}
      {data.actual_path && (
        <Polyline
          positions={data.actual_path}
          pathOptions={{ color: teamColor }}
          interactive={false}
        />
      )}
      {data.targets.map((t, idx) => (
        <CircleMarker
          key={`tgt-${idx}`}
          center={t.position}
          radius={6}
          pathOptions={{ color: TARGET, weight: 2, fill: false }}
          interactive={false}
        />
      ))}
    </>
  );
}

function TacticalOverlayIfSelected(props: {
  flight: Flight;
  selected: boolean;
}) {
  if (!props.selected) {
    return <></>;
  }
  return <TacticalOverlayLayer flight={props.flight} />;
}

export default function FlightPlan(props: FlightPlanProps) {
  return (
    <>
      <FlightPlanPath {...props} />
      <WaypointMarkers {...props} />
      <TacticalOverlayIfSelected
        flight={props.flight}
        selected={props.selected}
      />
    </>
  );
}
