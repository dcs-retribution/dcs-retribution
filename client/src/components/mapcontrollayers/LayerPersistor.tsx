import React from "react";
import { useMapEvents } from "react-leaflet";
import { useDispatch } from "react-redux";
import { setActiveBaseMap, setOverlayState } from "../../api/mapSlice";

export const LayerPersistor: React.FC = () => {
  const dispatch = useDispatch();

  useMapEvents({
    baselayerchange(e) {
      dispatch(setActiveBaseMap(e.name));
    },
    overlayadd(e) {
      dispatch(setOverlayState({ name: e.name, checked: true }));
    },
    overlayremove(e) {
      dispatch(setOverlayState({ name: e.name, checked: false }));
    },
  });

  return null;
};