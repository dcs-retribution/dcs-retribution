import { UnculledZone } from "../../api/liberationApi";
import { selectUnculledZones } from "../../api/unculledZonesSlice";
import { useAppSelector } from "../../app/hooks";
import { LayerGroup, Circle } from "react-leaflet";
import { MapOverlay } from "../mapcontrollayers/MapOverlay"

interface CullingExclusionCirclesProps {
  zones: UnculledZone[];
}

const CullingExclusionCircles = (props: CullingExclusionCirclesProps) => {
  return (
    <>
      <LayerGroup>
        {props.zones.map((zone, idx) => {
          return (
            <Circle
              key={idx}
              center={zone.position}
              radius={zone.radius}
              color="#b4ff8c"
              fill={false}
              interactive={false}
            />
          );
        })}
      </LayerGroup>
    </>
  );
};

export default function CullingExclusionZones() {
  const data = useAppSelector(selectUnculledZones).zones;

  return (
    <MapOverlay name="Culling exclusion zones">
      <CullingExclusionCircles zones={data}></CullingExclusionCircles>
    </MapOverlay>
  );
}
