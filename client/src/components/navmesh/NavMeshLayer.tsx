import {
  navMeshSelectionUpdated,
  selectNavMeshes,
} from "../../api/navMeshSlice";
import { useSetNavmeshSelectionMutation } from "../../api/liberationApi";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { Polygon as LeafletPolygon } from "leaflet";
import { useCallback, useEffect, useRef } from "react";
import { LayerGroup, Polygon } from "react-leaflet";

interface NavMeshLayerProps {
  blue: boolean;
}

interface NavMeshPolygonProps {
  id: number;
  positions: Array<Array<{ lat: number; lng: number }>>;
  threatened: boolean;
  selected: boolean;
  onToggle: (id: number) => void;
}

function NavMeshPolygon(props: NavMeshPolygonProps) {
  const polygonRef = useRef<LeafletPolygon | null>(null);

  const style = {
    color: props.selected ? "#000000" : "#4d4d4d",
    weight: props.selected ? 2 : 1,
    fillColor: props.threatened ? "#ff0000" : "#00ff00",
    fillOpacity: props.selected ? 0.25 : 0.1,
  };

  useEffect(() => {
    const polygon = polygonRef.current;
    if (!polygon) {
      return;
    }
    polygon.setStyle(style);
    if (props.selected) {
      polygon.bringToFront();
    }
  }, [props.selected, props.threatened, style]);

  useEffect(() => {
    const polygon = polygonRef.current;
    if (!polygon) {
      return;
    }
    const handleClick = () => props.onToggle(props.id);
    polygon.on("click", handleClick);
    return () => {
      polygon.off("click", handleClick);
    };
  }, [props.id, props.onToggle]);

  const handleClick = useCallback(
    () => props.onToggle(props.id),
    [props.id, props.onToggle]
  );

  return (
    <Polygon
      ref={polygonRef}
      positions={props.positions}
      className="navmesh-polygon"
      color={style.color}
      weight={style.weight}
      fill
      fillColor={style.fillColor}
      fillOpacity={style.fillOpacity}
      noClip
      interactive
      pane="navmesh"
      eventHandlers={{
        click: handleClick,
      }}
    />
  );
}

export default function NavMeshLayer(props: NavMeshLayerProps) {
  const dispatch = useAppDispatch();
  const meshes = useAppSelector(selectNavMeshes);
  const [setSelection] = useSetNavmeshSelectionMutation();
  const mesh = props.blue ? meshes.blue : meshes.red;
  const selection = props.blue ? meshes.blueSelection : meshes.redSelection;
  const selectionSet = new Set(selection);
  const toggleSelection = useCallback(
    (id: number) => {
      const nextSelection = selectionSet.has(id)
        ? selection.filter((selectedId) => selectedId !== id)
        : [...selection, id];
      const player = props.blue ? "Blue" : "Red";
      dispatch(
        navMeshSelectionUpdated({
          blue: props.blue,
          selection: nextSelection,
        })
      );
      setSelection({
        forPlayer: player,
        body: { poly_ids: nextSelection },
      });
    },
    [dispatch, props.blue, selection, selectionSet, setSelection]
  );
  return (
    <LayerGroup>
      {mesh.map((zone) => {
        return (
          <NavMeshPolygon
            key={zone.id}
            id={zone.id}
            positions={zone.poly}
            threatened={zone.threatened}
            selected={selectionSet.has(zone.id)}
            onToggle={toggleSelection}
          />
        );
      })}
    </LayerGroup>
  );
}
