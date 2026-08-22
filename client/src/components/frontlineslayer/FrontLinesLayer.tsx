import { selectFrontLines } from "../../api/frontLinesSlice";
import { useAppSelector } from "../../app/hooks";
import FrontLine from "../frontline";
import { LayerGroup, Pane } from "react-leaflet";

export default function FrontLinesLayer() {
  const fronts = useAppSelector(selectFrontLines).fronts;
  return (
    // Dedicated pane above the default overlayPane (z 400): blue flight plans
    // put a wide invisible hover polyline on top of everything in that pane,
    // which swallowed right-clicks on a front line crossing it (the browser
    // context menu appeared instead of the new-package dialog). Panes hit-test
    // in z order, so raising the fronts keeps their contextmenu reachable.
    // Still below the marker pane (z 600).
    <Pane name="front-lines" style={{ zIndex: 450 }}>
      <LayerGroup>
        {Object.values(fronts).map((front, idx) => {
          return <FrontLine key={idx} front={front} />;
        })}
      </LayerGroup>
    </Pane>
  );
}
