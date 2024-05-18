import { useGetTerrainZonesQuery } from "../../api/liberationApi";
import { useAppSelector } from "../../app/hooks";
import { LatLngLiteral } from "leaflet";
import { LayerGroup, LayersControl, Polygon } from "react-leaflet";
import { selectMapZones } from "../../api/mapZonesSlice";

interface TerrainZoneLayerProps {
  zones: LatLngLiteral[][][];
  color: string;
  fillColor: string;
}

function TerrainZoneLayer(props: TerrainZoneLayerProps) {
  return (
    <LayerGroup>
      {props.zones.map((poly, idx) => {
        return (
          <Polygon
            key={idx}
            positions={poly}
            color={props.color}
            fillColor={props.fillColor}
            fillOpacity={1}
            interactive={false}
          />
        );
      })}
    </LayerGroup>
  );
}

export default function TerrainZonesLayers() {
  const zones = useAppSelector(selectMapZones).mapZones;
  var exclusion = <></>;
  var inclusion = <></>;
  var sea = <></>;

  if (zones) {
    exclusion = (
      <TerrainZoneLayer
        zones={zones.exclusion}
        color="#969696"
        fillColor="#303030"
      />
    );
    inclusion = (
      <TerrainZoneLayer
        zones={zones.inclusion}
        color="#969696"
        fillColor="#4b4b4b"
      />
    );
    sea = (
      <TerrainZoneLayer zones={zones.sea} color="#344455" fillColor="#344455" />
    );
  }
  return (
    <>
      <LayersControl.Overlay name="Inclusion zones">
        {inclusion}
      </LayersControl.Overlay>
      <LayersControl.Overlay name="Exclusion zones">
        {exclusion}
      </LayersControl.Overlay>
      <LayersControl.Overlay name="Sea zones">{sea}</LayersControl.Overlay>
    </>
  );
}
