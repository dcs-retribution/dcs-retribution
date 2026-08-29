import React from "react";
import { render } from "@testing-library/react";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import mapReducer, {
  selectActiveBaseMap,
  selectOverlayChecked,
} from "../../api/mapSlice";
import { LayerPersistor } from "./LayerPersistor";

// Store event handlers registered via useMapEvents
let registeredEvents: Record<string, (e: any) => void> = {};

jest.mock("react-leaflet", () => ({
  useMapEvents: (handlers: Record<string, (e: any) => void>) => {
    registeredEvents = handlers;
    return null;
  },
}));

const createTestStore = () =>
  configureStore({
    reducer: { map: mapReducer },
  });

describe("LayerPersistor", () => {
  beforeEach(() => {
    registeredEvents = {};
  });

  it("registers leaflet map event listeners on mount", () => {
    const store = createTestStore();
    render(
      <Provider store={store}>
        <LayerPersistor />
      </Provider>
    );

    expect(registeredEvents).toHaveProperty("baselayerchange");
    expect(registeredEvents).toHaveProperty("overlayadd");
    expect(registeredEvents).toHaveProperty("overlayremove");
  });

  it("dispatches setActiveBaseMap on baselayerchange event", () => {
    const store = createTestStore();
    render(
      <Provider store={store}>
        <LayerPersistor />
      </Provider>
    );

    registeredEvents.baselayerchange({ name: "Topographic" });

    expect(selectActiveBaseMap(store.getState() as any)).toBe("Topographic");
  });

  it("dispatches setOverlayState with checked=true on overlayadd event", () => {
    const store = createTestStore();
    render(
      <Provider store={store}>
        <LayerPersistor />
      </Provider>
    );

    registeredEvents.overlayadd({ name: "Airfields" });

    expect(selectOverlayChecked("Airfields", false)(store.getState() as any)).toBe(true);
  });

  it("dispatches setOverlayState with checked=false on overlayremove event", () => {
    const store = createTestStore();
    render(
      <Provider store={store}>
        <LayerPersistor />
      </Provider>
    );

    registeredEvents.overlayadd({ name: "Airfields" });
    expect(selectOverlayChecked("Airfields", false)(store.getState() as any)).toBe(true);

    registeredEvents.overlayremove({ name: "Airfields" });

    expect(selectOverlayChecked("Airfields", false)(store.getState() as any)).toBe(false);
  });
});