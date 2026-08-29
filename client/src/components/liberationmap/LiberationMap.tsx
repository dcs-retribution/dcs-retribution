import { selectMapCenter } from "../../api/mapSlice";
import { useAppSelector } from "../../app/hooks";
import AircraftLayer from "../aircraftlayer";
import AirDefenseRangeLayer from "../airdefenserangelayer";
import EmitterHighlightToggle from "../airdefenserangelayer/EmitterHighlightToggle";
import CombatLayer from "../combatlayer";
import ControlPointsLayer from "../controlpointslayer";
import CullingExclusionZones from "../cullingexclusionzones/CullingExclusionZones";
import FlightPlansLayer from "../flightplanslayer";
import FrontLinesLayer from "../frontlineslayer";
import Iadsnetworklayer from "../iadsnetworklayer";
import NavMeshLayer from "../navmesh/NavMeshLayer";
import LeafletRuler from "../ruler/Ruler";
import SupplyRoutesLayer from "../supplyrouteslayer";
import TerrainZonesLayers from "../terrainzones/TerrainZonesLayers";
import TgosLayer from "../tgoslayer/TgosLayer";
import { CoalitionThreatZones } from "../threatzones";
import { WaypointDebugZonesControls } from "../waypointdebugzones/WaypointDebugZonesControls";
import "./LiberationMap.css";
import { Map } from "leaflet";
import { useEffect, useRef } from "react";
import { BasemapLayer } from "react-esri-leaflet";
import { LayersControl, MapContainer, ScaleControl, TileLayer } from "react-leaflet";
import { LayerPersistor } from "../mapcontrollayers/LayerPersistor";
import { MapBaseLayer } from "../mapcontrollayers/MapBaseLayer"
import { MapOverlay } from "../mapcontrollayers/MapOverlay"
import { BlendedTileLayer } from "../mapcontrollayers/BlendedTileLayer";


export default function LiberationMap() {
  const map = useRef<Map>(null);
  const mapCenter = useAppSelector(selectMapCenter);
  useEffect(() => {
    map.current?.setView(mapCenter, map.current?.getZoom() ?? 8, { animate: true, duration: 1 });
  });
  return (
    <MapContainer zoom={map.current?.getZoom() ?? 8} zoomControl={false} ref={map}>
      <ScaleControl />
      <LeafletRuler />
      <LayerPersistor />
      <LayersControl collapsed={false}>
        <MapBaseLayer name="Imagery Clarity" defaultChecked>
          <BasemapLayer name="ImageryClarity" />
        </MapBaseLayer>
        <MapBaseLayer name="Imagery Firefly">
          <BasemapLayer name="ImageryFirefly" />
        </MapBaseLayer>
        <MapBaseLayer name="Topographic">
          <BasemapLayer name="Topographic" />
        </MapBaseLayer>
        <MapBaseLayer name="Topographic (3D Relief)">
          <BlendedTileLayer
            baseUrl="https://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
            overlayUrl="https://services.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}"
            blendMode="multiply"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a> | Hillshade &copy; Esri'
          />
        </MapBaseLayer>
        <MapBaseLayer name="OpenStreetMap">
          <BlendedTileLayer
            baseUrl="https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png"
            overlayUrl="https://services.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}"
            blendMode="multiply"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a> | Hillshade &copy; Esri'
          />
        </MapBaseLayer>
        <MapBaseLayer name="OpenTopoMap">
          <TileLayer
            url="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
            maxZoom={17}
            attribution='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, SRTM | Map style: &copy; OpenTopoMap'
          />
        </MapBaseLayer>
        <MapBaseLayer name="Esri Dark Gray">
          <BlendedTileLayer
            baseUrl="https://services.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}"
            overlayUrl="https://services.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}"
            labelsUrl="https://services.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}"
            attribution="Tiles &copy; Esri &mdash; Esri, HERE, Garmin, FAO, NOAA, USGS"
            blendMode="screen"
            overlayFilter="invert(100%) contrast(120%) brightness(125%)"
            overlayOpacity={0.6}
          />
        </MapBaseLayer>
        <MapBaseLayer name="Tactical Dark OSM">
          <BlendedTileLayer
            baseUrl="https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png"
            overlayUrl="https://services.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Hillshade &copy; Esri'
            baseFilter="invert(100%) hue-rotate(180deg) brightness(0.9) contrast(150%)"
            blendMode="screen"
            overlayFilter="invert(100%) contrast(120%) brightness(120%)"
            overlayOpacity={0.6}
          />
        </MapBaseLayer>
        <MapOverlay name="Control points" defaultChecked={true}>
          <ControlPointsLayer />
        </MapOverlay>
        <MapOverlay name="Aircraft" defaultChecked={true}>
          <AircraftLayer />
        </MapOverlay>
        <MapOverlay name="Active combat" defaultChecked={true}>
          <CombatLayer />
        </MapOverlay>
        <MapOverlay name="Air defenses" defaultChecked={true}>
          <TgosLayer categories={["aa"]} />
        </MapOverlay>
        <MapOverlay name="LORAD" >
          <TgosLayer categories={["aa"]} task={"LORAD"} />
        </MapOverlay>
        <MapOverlay name="MERAD" >
          <TgosLayer categories={["aa"]} task={"MERAD"} />
        </MapOverlay>
        <MapOverlay name="SHORAD" >
          <TgosLayer categories={["aa"]} task={"SHORAD"} />
        </MapOverlay>
        <MapOverlay name="AAA" >
          <TgosLayer categories={["aa"]} task={"AAA"} />
        </MapOverlay>
        <MapOverlay name="Factories" defaultChecked={true}>
          <TgosLayer categories={["factory"]} />
        </MapOverlay>
        <MapOverlay name="Ships" defaultChecked={true}>
          <TgosLayer categories={["ship"]} />
        </MapOverlay>
        <MapOverlay name="Other ground objects" defaultChecked={true}>
          <TgosLayer categories={["aa", "factory", "ship"]} exclude />
        </MapOverlay>
        <MapOverlay name="Supply routes" defaultChecked={true}>
          <SupplyRoutesLayer />
        </MapOverlay>
        <MapOverlay name="Front lines" defaultChecked={true}>
          <FrontLinesLayer />
        </MapOverlay>
        <MapOverlay name="Enemy SAM threat range" defaultChecked={true}>
          <AirDefenseRangeLayer blue={false} />
        </MapOverlay>
        <MapOverlay name="Enemy SAM detection range">
          <AirDefenseRangeLayer blue={false} detection />
        </MapOverlay>
        <MapOverlay name="Enemy IADS Network">
          <Iadsnetworklayer blue={false} />
        </MapOverlay>
        <MapOverlay name="Allied SAM threat range">
          <AirDefenseRangeLayer blue={true} />
        </MapOverlay>
        <MapOverlay name="Allied SAM detection range">
          <AirDefenseRangeLayer blue={true} detection />
        </MapOverlay>
        <MapOverlay name="Highlight radar emitter on hover" defaultChecked={true}>
          <EmitterHighlightToggle />
        </MapOverlay>
        <MapOverlay name="Allied IADS Network">
          <Iadsnetworklayer blue={true} />
        </MapOverlay>
        <MapOverlay name="Selected flight plan">
          <FlightPlansLayer selectedOnly />
        </MapOverlay>
        <MapOverlay name="All blue flight plans" defaultChecked={true}>
          <FlightPlansLayer blue={true} />
        </MapOverlay>
        <MapOverlay name="All red flight plans">
          <FlightPlansLayer blue={false} />
        </MapOverlay>
      </LayersControl>
      <LayersControl position="topleft">
        <CoalitionThreatZones blue={true} />
        <CoalitionThreatZones blue={false} />
        <MapOverlay name="Blue navmesh">
          <NavMeshLayer blue={true} />
        </MapOverlay>
        <MapOverlay name="Red navmesh">
          <NavMeshLayer blue={false} />
        </MapOverlay>
        <TerrainZonesLayers />
        <CullingExclusionZones />
        <WaypointDebugZonesControls />
      </LayersControl>
    </MapContainer>
  );
}
