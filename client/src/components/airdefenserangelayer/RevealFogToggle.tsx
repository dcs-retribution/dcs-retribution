import backend from "../../api/backend";
import reloadGameState from "../../api/gamestate";
import { AppDispatch } from "../../app/store";
import { useAppDispatch } from "../../app/hooks";
import { LayerGroup } from "react-leaflet";

// Empty layer wrapped in a LayersControl.Overlay. Toggling the overlay flips the
// transient, server-side "reveal fog of war" flag, then re-pulls game state so the
// map redraws with (or without) the recon-fogged enemy composition, threat/
// detection rings, and IADS links. The flag is runtime-only and never persisted,
// so a save can never carry a god-view.
function setReveal(dispatch: AppDispatch, revealed: boolean) {
  backend
    .put("/fog-of-war/reveal", null, { params: { revealed } })
    .then(() => reloadGameState(dispatch, true))
    .catch((error) => console.log(`Error toggling fog of war: ${error}`));
}

export default function RevealFogToggle() {
  const dispatch = useAppDispatch();
  return (
    <LayerGroup
      eventHandlers={{
        add: () => setReveal(dispatch, true),
        remove: () => setReveal(dispatch, false),
      }}
    />
  );
}
