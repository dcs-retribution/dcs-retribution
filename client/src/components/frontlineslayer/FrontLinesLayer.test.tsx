import { renderWithProviders } from "../../testutils";
import FrontLinesLayer from "./FrontLinesLayer";
import { PropsWithChildren } from "react";

const mockPolyline = jest.fn();
const mockLayerGroup = jest.fn();
const mockPane = jest.fn();
jest.mock("react-leaflet", () => ({
  Pane: (props: PropsWithChildren<any>) => {
    mockPane(props);
    return <>{props.children}</>;
  },
  LayerGroup: (props: PropsWithChildren<any>) => {
    mockLayerGroup(props);
    return <>{props.children}</>;
  },
  Polyline: (props: any) => {
    mockPolyline(props);
  },
}));

// The waypoints in test data below should all use `should_make: false`. Markers
// need useMap() to check the zoom level to decide if they should be drawn or
// not, and we don't have good options here for mocking that behavior.
describe("FrontLinesLayer", () => {
  it("draws nothing when there are no front lines", () => {
    renderWithProviders(<FrontLinesLayer />);
    expect(mockPolyline).not.toHaveBeenCalled();
    expect(mockLayerGroup).toHaveBeenCalledTimes(1);
  });

  it("draws into a pane above the default overlay pane", () => {
    // Front lines live in their own pane so a flight plan's wide invisible hover
    // polyline (in the default overlayPane, z 400) cannot swallow a right-click
    // on a front line crossing it. Below the marker pane at z 600.
    renderWithProviders(<FrontLinesLayer />);
    expect(mockPane).toHaveBeenCalledWith(
      expect.objectContaining({
        name: "front-lines",
        style: { zIndex: 450 },
      })
    );
  });

  it("draws front lines", () => {
    const extents = [
      { lat: 0, lng: 0 },
      { lat: 1, lng: 1 },
    ];
    renderWithProviders(<FrontLinesLayer />, {
      preloadedState: {
        frontLines: {
          fronts: {
            foo: {
              id: "foo",
              extents: extents,
            },
            bar: {
              id: "bar",
              extents: extents,
            },
          },
        },
      },
    });
    expect(mockPolyline).toHaveBeenCalledTimes(2);
    expect(mockPolyline).toHaveBeenCalledWith(
      expect.objectContaining({
        positions: extents,
      })
    );
    expect(mockLayerGroup).toHaveBeenCalledTimes(1);
  });
});
