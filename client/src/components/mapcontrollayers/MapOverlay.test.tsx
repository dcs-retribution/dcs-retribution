import React from "react";
import { render, screen } from "@testing-library/react";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import mapReducer from "../../api/mapSlice";
import { MapOverlay } from "./MapOverlay";

// Mock react-leaflet to isolate wrapper logic and inspect rendered props
jest.mock("react-leaflet", () => ({
  LayersControl: {
    Overlay: ({
      name,
      checked,
      children,
    }: {
      name: string;
      checked: boolean;
      children: React.ReactNode;
    }) => (
      <div
        data-testid="leaflet-overlay"
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
  overlayStates: Record<string, boolean> = {}
) => {
  const store = configureStore({
    reducer: { map: mapReducer },
    preloadedState: {
      map: {
        center: { lat: 0, lng: 0 },
        hoveredEmitterId: null,
        hoveredEmitterSource: null,
        highlightEmitters: false, // <-- Added required property
        activeBaseMap: null,
        overlayStates,
      },
    },
  });

  return render(<Provider store={store}>{ui}</Provider>);
};

describe("MapOverlay", () => {
  it("renders children and sets name prop correctly", () => {
    renderWithRedux(
      <MapOverlay name="SAM Ranges">
        <span>SAM Circle Content</span>
      </MapOverlay>
    );

    const overlayEl = screen.getByTestId("leaflet-overlay");
    expect(overlayEl).toHaveAttribute("data-name", "SAM Ranges");
    expect(screen.getByText("SAM Circle Content")).toBeInTheDocument();
  });

    it("falls back to defaultChecked=false when overlay state is unset and no prop provided", () => {
    renderWithRedux(
        <MapOverlay name="SAM Ranges">
        <div />
        </MapOverlay>
    );

    const overlayEl = screen.getByTestId("leaflet-overlay");
    expect(overlayEl.getAttribute("data-checked")).toBe("false");
    });

    it("respects custom defaultChecked=true prop when overlay state is unset", () => {
    renderWithRedux(
        <MapOverlay name="SAM Ranges" defaultChecked={true}>
        <div />
        </MapOverlay>
    );

    const overlayEl = screen.getByTestId("leaflet-overlay");
    expect(overlayEl.getAttribute("data-checked")).toBe("true");
    });

  it("uses saved Redux state when overlay name exists in store (checked: true)", () => {
    renderWithRedux(
      <MapOverlay name="SAM Ranges" defaultChecked={false}>
        <div />
      </MapOverlay>,
      { "SAM Ranges": true }
    );

    const overlayEl = screen.getByTestId("leaflet-overlay");
    expect(overlayEl.getAttribute("data-checked")).toBe("true");
  });

  it("uses saved Redux state when overlay name exists in store (checked: false)", () => {
    renderWithRedux(
      <MapOverlay name="SAM Ranges" defaultChecked={true}>
        <div />
      </MapOverlay>,
      { "SAM Ranges": false }
    );

    const overlayEl = screen.getByTestId("leaflet-overlay");
    expect(overlayEl.getAttribute("data-checked")).toBe("false");
  });
});