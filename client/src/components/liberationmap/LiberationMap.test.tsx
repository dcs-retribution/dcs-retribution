import React from "react";
import { render, screen } from "@testing-library/react";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import mapReducer from "../../api/mapSlice";
import LiberationMap from "./LiberationMap";

// Mock Map object reference
const mockSetView = jest.fn();
const mockGetZoom = jest.fn(() => 8);
const mockMap = {
  setView: mockSetView,
  getZoom: mockGetZoom,
};

// Mock Leaflet and React-Leaflet
jest.mock("react-leaflet", () => {
  const React = require("react");

  return {
    MapContainer: React.forwardRef(({ children }: any, ref: any) => {
      if (ref) {
        if (typeof ref === "function") ref(mockMap);
        else ref.current = mockMap;
      }
      return <div data-testid="map-container">{children}</div>;
    }),
    ScaleControl: () => <div data-testid="scale-control" />,
    LayerGroup: ({ children }: any) => <div data-testid="layer-group">{children}</div>,
    TileLayer: ({ url }: { url: string }) => <div data-testid="tile-layer" data-url={url} />,
    LayersControl: Object.assign(
      ({ children, position }: any) => (
        <div data-testid="layers-control" data-position={position || "topright"}>
          {children}
        </div>
      ),
      {
        BaseLayer: ({ name, checked, children }: any) => (
          <div data-testid="leaflet-base-layer" data-name={name} data-checked={checked}>
            {children}
          </div>
        ),
        Overlay: ({ name, checked, children }: any) => (
          <div data-testid="leaflet-overlay" data-name={name} data-checked={checked}>
            {children}
          </div>
        ),
      }
    ),
    useMap: () => mockMap,
  };
});

// Mock BlendedTileLayer to prevent HTMLCanvasElement context issues in JSDOM
jest.mock("../mapcontrollayers/BlendedTileLayer", () => ({
  BlendedTileLayer: () => <div data-testid="blended-tile-layer" />,
}));

// Mock Esri Basemap
jest.mock("react-esri-leaflet", () => ({
  BasemapLayer: ({ name }: { name: string }) => <div data-testid={`esri-basemap-${name}`} />,
}));

// Mock Leaflet Ruler and LayerPersistor
jest.mock("../ruler/Ruler", () => () => <div data-testid="leaflet-ruler" />);
jest.mock("../mapcontrollayers/LayerPersistor", () => ({
  LayerPersistor: () => <div data-testid="layer-persistor" />,
}));

// Mock child layer components to avoid rendering heavy domain layer logic
jest.mock("../controlpointslayer", () => () => <div data-testid="layer-control-points" />);
jest.mock("../aircraftlayer", () => () => <div data-testid="layer-aircraft" />);
jest.mock("../combatlayer", () => () => <div data-testid="layer-combat" />);
jest.mock("../tgoslayer/TgosLayer", () => () => <div data-testid="layer-tgos" />);
jest.mock("../supplyrouteslayer", () => () => <div data-testid="layer-supply-routes" />);
jest.mock("../frontlineslayer", () => () => <div data-testid="layer-front-lines" />);
jest.mock("../airdefenserangelayer", () => () => <div data-testid="layer-air-defense" />);
jest.mock("../airdefenserangelayer/EmitterHighlightToggle", () => () => <div data-testid="emitter-toggle" />);
jest.mock("../iadsnetworklayer", () => () => <div data-testid="layer-iads" />);
jest.mock("../flightplanslayer", () => () => <div data-testid="layer-flight-plans" />);
jest.mock("../threatzones", () => ({ CoalitionThreatZones: () => <div data-testid="layer-threat-zones" /> }));
jest.mock("../navmesh/NavMeshLayer", () => () => <div data-testid="layer-navmesh" />);
jest.mock("../terrainzones/TerrainZonesLayers", () => () => <div data-testid="layer-terrain-zones" />);
jest.mock("../cullingexclusionzones/CullingExclusionZones", () => () => <div data-testid="layer-culling-zones" />);
jest.mock("../waypointdebugzones/WaypointDebugZonesControls", () => ({
  WaypointDebugZonesControls: () => <div data-testid="layer-waypoint-debug" />,
}));

const renderWithRedux = (ui: React.ReactElement, initialMapState = {}) => {
  const store = configureStore({
    reducer: { map: mapReducer },
    preloadedState: {
      map: {
        center: { lat: 42.0, lng: 43.0 },
        hoveredEmitterId: null,
        hoveredEmitterSource: null,
        highlightEmitters: false,
        activeBaseMap: null,
        overlayStates: {},
        ...initialMapState,
      },
    },
  });

  return render(<Provider store={store}>{ui}</Provider>);
};

describe("LiberationMap", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders map container, scale control, ruler, and layer persistor", () => {
    renderWithRedux(<LiberationMap />);

    expect(screen.getByTestId("map-container")).toBeInTheDocument();
    expect(screen.getByTestId("scale-control")).toBeInTheDocument();
    expect(screen.getByTestId("leaflet-ruler")).toBeInTheDocument();
    expect(screen.getByTestId("layer-persistor")).toBeInTheDocument();
  });

  it("renders updated basemap layers within LayersControl", () => {
    renderWithRedux(<LiberationMap />);

    const baseLayers = screen.getAllByTestId("leaflet-base-layer");
    const names = baseLayers.map((el) => el.getAttribute("data-name"));

    expect(names).toEqual([
      "Imagery Clarity",
      "Imagery Firefly",
      "Topographic",
      "Topographic (3D Relief)",
      "OpenStreetMap",
      "OpenTopoMap",
      "Esri Dark Gray",
      "Tactical Dark OSM",
    ]);
  });

  it("renders expected overlay options within LayersControl", () => {
    renderWithRedux(<LiberationMap />);

    const overlays = screen.getAllByTestId("leaflet-overlay");
    const names = overlays.map((el) => el.getAttribute("data-name"));

    expect(names).toContain("Control points");
    expect(names).toContain("Aircraft");
    expect(names).toContain("Active combat");
    expect(names).toContain("Front lines");
    expect(names).toContain("Enemy SAM threat range");
    expect(names).toContain("Blue navmesh");
    expect(names).toContain("Red navmesh");
  });

  it("updates map view via setView when map center state changes", () => {
    renderWithRedux(<LiberationMap />, {
      center: { lat: 45.0, lng: 38.0 },
    });

    expect(mockSetView).toHaveBeenCalledWith(
      { lat: 45.0, lng: 38.0 },
      8,
      { animate: true, duration: 1 }
    );
  });
});