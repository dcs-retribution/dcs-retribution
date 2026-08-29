import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";
import { LatLngLiteral } from "leaflet";

// Where a hover originated: the emitter's icon, or one of its range rings. The
// highlight is symmetric (hovering either lights up the other), but hovering a
// ring also marks its emitter with a blob so you can find it; hovering the
// emitter does not blob the icon you're already pointing at.
export type EmitterHoverSource = "emitter" | "ring";

const BASEMAP_STORAGE_KEY = "active_basemap_layer";
const OVERLAYS_STORAGE_KEY = "active_map_overlays";

const safeGetItem = (key: string): string | null => {
  try {
    return localStorage.getItem(key);
  } catch (error) {
    console.warn(`localStorage read failed for key "${key}":`, error);
    return null;
  }
};

const safeSetItem = (key: string, value: string): void => {
  try {
    localStorage.setItem(key, value);
  } catch (error) {
    console.warn(`localStorage write failed for key "${key}":`, error);
  }
};

const loadSavedOverlays = (): Record<string, boolean> => {
  const saved = safeGetItem(OVERLAYS_STORAGE_KEY);
  if (!saved) return {};
  try {
    return JSON.parse(saved);
  } catch (error) {
    console.warn("Failed to parse saved map overlays JSON:", error);
    return {};
  }
};

interface MapState {
  center: LatLngLiteral;
  // Id of the TGO whose air-defense ring (or icon) is currently hovered, so its
  // icon can be raised above overlapping ones while highlighted.
  hoveredEmitterId: string | null;
  // What was hovered to set hoveredEmitterId (icon vs. ring).
  hoveredEmitterSource: EmitterHoverSource | null;
  // Whether the hover highlight (ring <-> emitter) is enabled. Toggled from
  // the map's layer control.
  highlightEmitters: boolean;
  // Persistent Map type 
  activeBaseMap: string | null;
  // Persistent Map options
  overlayStates: Record<string, boolean>;
}

const initialState: MapState = {
  center: { lat: 0, lng: 0 },
  hoveredEmitterId: null,
  hoveredEmitterSource: null,
  highlightEmitters: true,
  activeBaseMap: localStorage.getItem(BASEMAP_STORAGE_KEY),
  overlayStates: loadSavedOverlays(),
};

const mapSlice = createSlice({
  name: "map",
  initialState: initialState,
  reducers: {
    setHoveredEmitter(
      state,
      action: PayloadAction<
        { id: string; source: EmitterHoverSource } | null
      >
    ) {
      state.hoveredEmitterId = action.payload?.id ?? null;
      state.hoveredEmitterSource = action.payload?.source ?? null;
    },
    setHighlightEmitters(state, action: PayloadAction<boolean>) {
      state.highlightEmitters = action.payload;
    },
    setActiveBaseMap(state, action: PayloadAction<string>) {
      state.activeBaseMap = action.payload;
      safeSetItem(BASEMAP_STORAGE_KEY, action.payload);
    },
    setOverlayState(
      state,
      action: PayloadAction<{ name: string; checked: boolean }>
    ) {
      const { name, checked } = action.payload;
      state.overlayStates[name] = checked;
      localStorage.setItem(OVERLAYS_STORAGE_KEY, JSON.stringify(state.overlayStates));
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      if (action.payload.map_center != null) {
        state.center = action.payload.map_center;
      }
    });
    builder.addCase(gameUnloaded, (state) => {
      state.center = { lat: 0, lng: 0 };
      state.hoveredEmitterId = null;
      state.hoveredEmitterSource = null;
    });
  },
});

export const { setHoveredEmitter, setHighlightEmitters, setActiveBaseMap, setOverlayState , } = mapSlice.actions;

export const selectMapCenter = (state: RootState) => state.map.center;
export const selectHoveredEmitter = (state: RootState) =>
  state.map.hoveredEmitterId;
export const selectHoveredEmitterSource = (state: RootState) =>
  state.map.hoveredEmitterSource;
export const selectHighlightEmitters = (state: RootState) =>
  state.map.highlightEmitters;
export const selectActiveBaseMap = (state: RootState) =>
  state.map.activeBaseMap;
export const selectOverlayChecked =
  (name: string, defaultChecked: boolean = false) =>
  (state: RootState): boolean =>
    state.map.overlayStates?.[name] ?? defaultChecked;
  
export default mapSlice.reducer;
