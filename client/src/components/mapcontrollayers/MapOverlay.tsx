import React from "react";
import { LayersControl } from "react-leaflet";
import { useSelector } from "react-redux";
import { selectOverlayChecked } from "../../api/mapSlice";

interface MapOverlayProps {
  name: string;
  defaultChecked?: boolean;
  children: React.ReactNode;
}

export const MapOverlay: React.FC<MapOverlayProps> = ({
  name,
  defaultChecked = false,
  children,
}) => {
  const isChecked = useSelector(selectOverlayChecked(name, defaultChecked));

  return (
    <LayersControl.Overlay name={name} checked={isChecked}>
      {children}
    </LayersControl.Overlay>
  );
};