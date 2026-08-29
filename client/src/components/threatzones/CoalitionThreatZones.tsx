import { ThreatZoneFilter, ThreatZonesLayer } from "./ThreatZonesLayer";
import { MapOverlay } from "../mapcontrollayers/MapOverlay"

interface CoalitionThreatZonesProps {
  blue: boolean;
}

export function CoalitionThreatZones(props: CoalitionThreatZonesProps) {
  const color = props.blue ? "Blue" : "Red";
  return (
    <>
      <MapOverlay name={`${color} threat zones: full`}>
        <ThreatZonesLayer blue={props.blue} filter={ThreatZoneFilter.FULL} />
      </MapOverlay>
      <MapOverlay name={`${color} threat zones: aircraft`}>
        <ThreatZonesLayer
          blue={props.blue}
          filter={ThreatZoneFilter.AIRCRAFT}
        />
      </MapOverlay>
      <MapOverlay name={`${color} threat zones: air defenses`}>
        <ThreatZonesLayer
          blue={props.blue}
          filter={ThreatZoneFilter.AIR_DEFENSES}
        />
      </MapOverlay>
      <MapOverlay name={`${color} threat zones: radar SAMs`}>
        <ThreatZonesLayer
          blue={props.blue}
          filter={ThreatZoneFilter.RADAR_SAMS}
        />
      </MapOverlay>
    </>
  );
}
