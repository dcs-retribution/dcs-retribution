import React from "react";
import { render, screen } from "@testing-library/react";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import mapReducer from "../../api/mapSlice";
import { MapBaseLayer } from "./MapBaseLayer";

// Mock react-leaflet to isolate component logic and inspect rendered props
jest.mock("react-leaflet", () => ({
  LayersControl: {
    BaseLayer: ({
      name,
      checked,
      children,
    }: {
      name: string;
      checked: boolean;
      children: React.ReactNode;
    }) => (
      <div
        data-testid="leaflet-base-layer"
        data-name={name}
        data-checked={checked}
      >
        {children}
      </div>
    ),
  },
}));

const renderWithRedux = (
  ui: React.ReactElement,
  initialState?: { activeBaseMap?: string | null }
) => {
  const store = configureStore({
    reducer: { map: mapReducer },
    preloadedState: {
      map: {
        center: { lat: 0, lng: 0 },
        hoveredEmitterId: null,
        hoveredEmitterSource: null,
        highlightEmitters: false,
        overlayStates: {},
        activeBaseMap: initialState?.activeBaseMap ?? null, // Guarantees string | null
      },
    },
  });

  return render(<Provider store={store}>{ui}</Provider>);
};

describe("MapBaseLayer", () => {
  it("renders children and correctly sets name prop", () => {
    renderWithRedux(
      <MapBaseLayer name="Satellite">
        <span>Tile Layer Content</span>
      </MapBaseLayer>
    );

    const layerEl = screen.getByTestId("leaflet-base-layer");
    expect(layerEl).toHaveAttribute("data-name", "Satellite");
    expect(screen.getByText("Tile Layer Content")).toBeInTheDocument();
  });

  it("falls back to defaultChecked=false when activeBaseMap is null", () => {
    renderWithRedux(
      <MapBaseLayer name="Satellite">
        <div />
      </MapBaseLayer>,
      { activeBaseMap: null }
    );

    const layerEl = screen.getByTestId("leaflet-base-layer");
    expect(layerEl.getAttribute("data-checked")).toBe("false");
  });

  it("falls back to defaultChecked=true when activeBaseMap is null", () => {
    renderWithRedux(
      <MapBaseLayer name="Imagery Clarity" defaultChecked>
        <div />
      </MapBaseLayer>,
      { activeBaseMap: null }
    );

    const layerEl = screen.getByTestId("leaflet-base-layer");
    expect(layerEl.getAttribute("data-checked")).toBe("true");
  });

  it("sets checked=true when activeBaseMap matches layer name", () => {
    renderWithRedux(
      <MapBaseLayer name="Topographic">
        <div />
      </MapBaseLayer>,
      { activeBaseMap: "Topographic" }
    );

    const layerEl = screen.getByTestId("leaflet-base-layer");
    expect(layerEl.getAttribute("data-checked")).toBe("true");
  });

  it("sets checked=false when activeBaseMap matches a different layer name (overriding defaultChecked)", () => {
    renderWithRedux(
      <MapBaseLayer name="Imagery Clarity" defaultChecked>
        <div />
      </MapBaseLayer>,
      { activeBaseMap: "Topographic" }
    );

    const layerEl = screen.getByTestId("leaflet-base-layer");
    expect(layerEl.getAttribute("data-checked")).toBe("false");
  });
});
