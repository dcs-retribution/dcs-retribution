import {
  useOpenNewTgoPackageDialogMutation,
  useOpenTgoInfoDialogMutation,
} from "../../api/liberationApi";
import { Tgo as TgoModel } from "../../api/liberationApi";
import {
  selectHighlightEmitters,
  selectHoveredEmitter,
  setHoveredEmitter,
} from "../../api/mapSlice";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import MobileTgo from "./MobileTgo";
import { TgoTooltip, iconForTgo } from "./shared";
import { Marker } from "react-leaflet";

interface TgoProps {
  tgo: TgoModel;
}

function StaticTgo(props: TgoProps) {
  const [openNewPackageDialog] = useOpenNewTgoPackageDialogMutation();
  const [openInfoDialog] = useOpenTgoInfoDialogMutation();
  const dispatch = useAppDispatch();
  // Raised above other icons while this emitter (or its ring) is hovered.
  const raised = useAppSelector(
    (state) =>
      selectHighlightEmitters(state) &&
      selectHoveredEmitter(state) === props.tgo.id
  );
  return (
    <Marker
      position={props.tgo.position}
      icon={iconForTgo(props.tgo)}
      zIndexOffset={raised ? 10000 : 0}
      eventHandlers={{
        click: () => {
          openInfoDialog({ tgoId: props.tgo.id });
        },
        contextmenu: () => {
          openNewPackageDialog({ tgoId: props.tgo.id });
        },
        // Hovering the emitter highlights its ring (and vice versa).
        mouseover: () =>
          dispatch(setHoveredEmitter({ id: props.tgo.id, source: "emitter" })),
        mouseout: () => dispatch(setHoveredEmitter(null)),
      }}
    >
      <TgoTooltip tgo={props.tgo} />
    </Marker>
  );
}

export default function Tgo(props: TgoProps) {
  if (props.tgo.mobile) {
    return <MobileTgo tgo={props.tgo} />;
  }
  return <StaticTgo tgo={props.tgo} />;
}
