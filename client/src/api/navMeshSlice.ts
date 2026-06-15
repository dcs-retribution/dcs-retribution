import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { NavMesh, NavMeshPoly } from "./liberationApi";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface NavMeshState {
  blue: NavMeshPoly[];
  red: NavMeshPoly[];
  blueSelection: number[];
  redSelection: number[];
}

const initialState: NavMeshState = {
  blue: [],
  red: [],
  blueSelection: [],
  redSelection: [],
};

export interface INavMeshUpdate {
  blue: boolean;
  mesh: NavMesh;
}

export interface INavMeshSelectionUpdate {
  blue: boolean;
  selection: number[];
}

const navMeshSlice = createSlice({
  name: "navmesh",
  initialState: initialState,
  reducers: {
    updated: (state, action: PayloadAction<INavMeshUpdate[]>) => {
      for (const [blue, navmesh] of Object.entries(action.payload)) {
        const data = {blue: (blue === "true"), mesh: navmesh} as unknown as INavMeshUpdate
        const polys = data.mesh.polys;
        if (data.blue) {
          state.blue = polys;
        } else {
          state.red = polys;
        }
      }
    },
    selectionUpdated: (state, action: PayloadAction<INavMeshSelectionUpdate>) => {
      if (action.payload.blue) {
        state.blueSelection = action.payload.selection;
      } else {
        state.redSelection = action.payload.selection;
      }
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.blue = action.payload.navmeshes.blue.polys;
      state.red = action.payload.navmeshes.red.polys;
      state.blueSelection = action.payload.navmesh_selection.blue;
      state.redSelection = action.payload.navmesh_selection.red;
    });
    builder.addCase(gameUnloaded, (state) => {
      state.blue = [];
      state.red = [];
      state.blueSelection = [];
      state.redSelection = [];
    });
  },
});

export const {
  updated: navMeshUpdated,
  selectionUpdated: navMeshSelectionUpdated,
} = navMeshSlice.actions;

export const selectNavMeshes = (state: RootState) => state.navmeshes;

export default navMeshSlice.reducer;
