import {
  AggregateGroundUnitEntry,
  Tgo as TgoModel,
} from "../../api/liberationApi";
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

export function formatInventory(inventory: string[]): string {
  return inventory.length ? inventory.join("\n") : "None";
}

function formatAggregateInventory(
  inventory: AggregateGroundUnitEntry[],
): string {
  return formatInventory(
    inventory.map((entry) => `${entry.count} × ${entry.display_name}`),
  );
}

function InventorySection(props: { label: string; inventory: string }) {
  return (
    <>
      {props.label}:
      {props.inventory === "None" ? (
        <>
          {" None"}
          <br />
        </>
      ) : (
        <>
          <br />
          <SplitLines items={props.inventory.split("\n")} />
        </>
      )}
    </>
  );
}

export function TgoTooltipContent(props: { tgo: TgoModel }) {
  const reserve = formatInventory(props.tgo.reserve_units ?? []);
  const expected = formatAggregateInventory(props.tgo.expected_inventory ?? []);
  const unrendered = formatAggregateInventory(
    props.tgo.unrendered_reserve ?? [],
  );
  const transit = formatAggregateInventory(props.tgo.in_transit_units ?? []);
  const units = props.tgo.units;

  return (
    <>
      {`${props.tgo.name} (${props.tgo.control_point_name})`}
      <br />
      {props.tgo.category === "motorpool" ? (
        <>
          <InventorySection label="Motorpool reserve" inventory={reserve} />
          <InventorySection label="Expected next turn" inventory={expected} />
          <InventorySection label="Unrendered reserve" inventory={unrendered} />
          <InventorySection label="In transit" inventory={transit} />
        </>
      ) : (
        <SplitLines items={units} />
      )}
    </>
  );
}

export function TgoTooltip(props: { tgo: TgoModel }) {
  return (
    <Tooltip>
      <TgoTooltipContent tgo={props.tgo} />
    </Tooltip>
  );
}
