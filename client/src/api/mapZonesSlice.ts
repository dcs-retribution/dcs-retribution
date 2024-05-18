import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { createSlice } from "@reduxjs/toolkit";
import { LatLngLiteral } from "leaflet";
import { MapZones } from "./_liberationApi";

interface MapZonesState {
  mapZones: MapZones;
}

const initialState: MapZonesState = {
  mapZones: { inclusion: [], exclusion: [], sea: [] },
};

const mapZonesSlice = createSlice({
  name: "map",
  initialState: initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      if (action.payload != null) {
        state.mapZones.exclusion = action.payload.map_zones.exclusion;
        state.mapZones.inclusion = action.payload.map_zones.inclusion;
        state.mapZones.sea = action.payload.map_zones.sea;
      }
    });
    builder.addCase(gameUnloaded, (state) => {
      state.mapZones = initialState.mapZones;
    });
  },
});

export const selectMapZones = (state: RootState) => state.mapZones;

export default mapZonesSlice.reducer;
