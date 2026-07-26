import { selectDownedPilots } from "../../api/downedPilotsSlice";
import { useAppSelector } from "../../app/hooks";
import DownedPilot from "../downedpilots/DownedPilot";
import { LayerGroup } from "react-leaflet";

export default function DownedPilotsLayer() {
  const downedPilots = Object.values(
    useAppSelector(selectDownedPilots).downedPilots
  );
  return (
    <LayerGroup>
      {downedPilots.map((downedPilot) => {
        return (
          <DownedPilot key={downedPilot.id} downedPilot={downedPilot} />
        );
      })}
    </LayerGroup>
  );
}
