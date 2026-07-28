import { selectDownedPilots } from "../../api/downedPilotsSlice";
import { useAppSelector } from "../../app/hooks";
import DownedPilot from "../downedpilots/DownedPilot";
import { LayerGroup } from "react-leaflet";

interface DownedPilotsLayerProps {
  // Which coalition's downed pilots to draw. Blue and red get their own map
  // overlays so either side can be toggled independently.
  blue: boolean;
}

export default function DownedPilotsLayer(props: DownedPilotsLayerProps) {
  const downedPilots = Object.values(
    useAppSelector(selectDownedPilots).downedPilots
  ).filter((downedPilot) => downedPilot.blue === props.blue);
  return (
    <LayerGroup>
      {downedPilots.map((downedPilot) => {
        return <DownedPilot key={downedPilot.id} downedPilot={downedPilot} />;
      })}
    </LayerGroup>
  );
}
