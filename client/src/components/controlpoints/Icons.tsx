import { ControlPoint } from "../../api/_liberationApi";
import { Icon, Point } from "leaflet";
import ms from "milsymbol";

export const iconForControlPoint = (cp: ControlPoint) => {
  const symbol = new ms.Symbol(cp.sidc, {
    size: 24,
    colorMode: "Dark",
  });

  return new Icon({
    iconUrl: symbol.toDataURL(),
    iconAnchor: new Point(symbol.getAnchor().x, symbol.getAnchor().y),
  });
};
