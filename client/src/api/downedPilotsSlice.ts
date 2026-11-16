import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { DownedPilot } from "./liberationApi";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

interface DownedPilotsState {
  downedPilots: { [key: string]: DownedPilot };
}

const initialState: DownedPilotsState = {
  downedPilots: {},
};

export const downedPilotsSlice = createSlice({
  name: "downedPilots",
  initialState,
  reducers: {
    updateDownedPilot: (state, action: PayloadAction<DownedPilot[]>) => {
      for (const pilot of action.payload) {
        state.downedPilots[pilot.id] = pilot;
      }
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.downedPilots = (action.payload.downed_pilots ?? []).reduce(
        (acc: { [key: string]: DownedPilot }, curr) => {
          acc[curr.id] = curr;
          return acc;
        },
        {}
      );
    });
    builder.addCase(gameUnloaded, (state) => {
      state.downedPilots = {};
    });
  },
});

export const { updateDownedPilot } = downedPilotsSlice.actions;

export const selectDownedPilots = (state: RootState) => state.downedPilots;

export default downedPilotsSlice.reducer;
