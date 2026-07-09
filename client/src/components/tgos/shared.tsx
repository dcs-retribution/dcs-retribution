import { Tgo as TgoModel } from "../../api/liberationApi";
import SplitLines from "../splitlines/SplitLines";
import { Icon, Point } from "leaflet";
import ms from "milsymbol";
import { Tooltip } from "react-leaflet";

export function iconForTgo(tgo: TgoModel) {
  const symbol = new ms.Symbol(tgo.sidc, { size: 24 });
  return new Icon({
    iconUrl: symbol.toDataURL(),
    iconAnchor: new Point(symbol.getAnchor().x, symbol.getAnchor().y),
  });
}

export function TgoTooltip(props: { tgo: TgoModel }) {
  return (
    <Tooltip>
      {`${props.tgo.name} (${props.tgo.control_point_name})`}
      <br />
      <SplitLines items={props.tgo.units} />
    </Tooltip>
  );
}
