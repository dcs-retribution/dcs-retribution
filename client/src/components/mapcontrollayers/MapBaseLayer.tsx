import React from "react";
import { LayersControl } from "react-leaflet";
import { useSelector } from "react-redux";
import { selectActiveBaseMap } from "../../api/mapSlice";

interface MapBaseLayerProps {
  name: string;
  defaultChecked?: boolean;
  children: React.ReactNode;
}

export const MapBaseLayer: React.FC<MapBaseLayerProps> = ({ name, defaultChecked = false, children }) => {
  const activeBaseMap = useSelector(selectActiveBaseMap);

const isChecked =
    activeBaseMap !== null ? activeBaseMap === name : defaultChecked;

  return (
    <LayersControl.BaseLayer name={name} checked={isChecked}>
      {children}
    </LayersControl.BaseLayer>
  );
};