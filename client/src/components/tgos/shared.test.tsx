import { render } from "@testing-library/react";
import { Tgo as TgoModel } from "../../api/liberationApi";
import { renderWithProviders } from "../../testutils";
import { waitFor } from "@testing-library/react";
import MobileTgo from "./MobileTgo";
import { formatInventory, TgoTooltip } from "./shared";

const mockMarker = jest.fn((_props: any) => null);
jest.mock("react-leaflet", () => ({
  Marker: (props: any) => {
    mockMarker(props);
    return null;
  },
  Polyline: () => null,
  Tooltip: ({ children }: { children: React.ReactNode }) => (
    <div>{children}</div>
  ),
}));

jest.mock("../../api/liberationApi", () => ({
  useClearTgoDestinationMutation: () => [jest.fn()],
  useOpenNewTgoPackageDialogMutation: () => [jest.fn()],
  useOpenTgoInfoDialogMutation: () => [jest.fn()],
  useSetTgoDestinationMutation: () => [jest.fn(), { isLoading: false }],
}));

const tgo = (overrides: Partial<TgoModel> = {}): TgoModel => ({
  id: "tgo-id",
  name: "Motorpool",
  control_point_name: "Base",
  category: "motorpool",
  blue: true,
  position: { lat: 0, lng: 0 },
  units: [],
  reserve_units: ["2228 | M1 Abrams", "2229 | M1 Abrams"],
  expected_inventory: [
    {
      unit_type: "M-1 Abrams",
      display_name: "M1 Abrams",
      count: 2,
    },
  ],
  unrendered_reserve: [],
  in_transit_units: [],
  threat_ranges: [],
  detection_ranges: [],
  dead: false,
  sidc: "SFGPUCI----K---",
  mobile: false,
  ...overrides,
});

describe("formatInventory", () => {
  it("returns None for an empty inventory", () => {
    expect(formatInventory([])).toBe("None");
  });

  it("preserves one row for every unit, including duplicate types", () => {
    expect(formatInventory(["2229 | M1 Abrams", "2228 | M1 Abrams"])).toBe(
      "2229 | M1 Abrams\n2228 | M1 Abrams",
    );
  });
});

describe("TgoTooltip", () => {
  it("renders count-only motorpool aggregates without fabricated ids", () => {
    const { container } = render(
      <TgoTooltip
        tgo={tgo({
          reserve_units: ["2228 | M1 Abrams"],
          unrendered_reserve: [
            { unit_type: "M-1 Abrams", display_name: "M1 Abrams", count: 3 },
          ],
          in_transit_units: [
            { unit_type: "M-2 Bradley", display_name: "M2 Bradley", count: 2 },
          ],
        })}
      />,
    );

    expect(container.innerHTML).toContain(
      "Motorpool reserve:<br>2228 | M1 Abrams<br>Expected next turn:<br>2 × M1 Abrams<br>Unrendered reserve:<br>3 × M1 Abrams<br>In transit:<br>2 × M2 Bradley",
    );
    expect(container.textContent).not.toContain("0001 |");
    expect(container.textContent).not.toContain("0002 |");
  });

  it("keeps empty reserve, unrendered, and transit inventories compact", () => {
    const { container } = render(
      <TgoTooltip
        tgo={tgo({
          reserve_units: [],
          expected_inventory: [],
          unrendered_reserve: [],
          in_transit_units: [],
        })}
      />,
    );

    expect(container.innerHTML).toContain(
      "Motorpool reserve: None<br>Expected next turn: None<br>Unrendered reserve: None<br>In transit: None",
    );
    expect(container.innerHTML).not.toContain("Motorpool reserve:<br>None");
    expect(container.innerHTML).not.toContain("Unrendered reserve:<br>None");
    expect(container.innerHTML).not.toContain("In transit:<br>None");
  });

  it("updates a mobile TGO marker when its streamed destination changes", async () => {
    const firstDestination = { lat: 1, lng: 2 };
    const secondDestination = { lat: 3, lng: 4 };
    const initialTgo = tgo({
      mobile: true,
      position: { lat: 0, lng: 0 },
      destination: firstDestination,
    });
    const { rerender } = renderWithProviders(<MobileTgo tgo={initialTgo} />);

    expect(
      mockMarker.mock.calls.some(
        ([props]) => props?.position === firstDestination,
      ),
    ).toBe(true);

    rerender(
      <MobileTgo tgo={{ ...initialTgo, destination: secondDestination }} />,
    );

    await waitFor(() => {
      expect(
        mockMarker.mock.calls.some(
          ([props]) => props?.position === secondDestination,
        ),
      ).toBe(true);
    });
  });

  it("keeps legacy units for non-motorpool TGOs", () => {
    render(
      <TgoTooltip
        tgo={tgo({
          category: "ship",
          units: ["F-16C"],
          reserve_units: [],
          unrendered_reserve: [],
          in_transit_units: [],
        })}
      />,
    );

    expect(document.body.textContent).toContain("F-16C");
    expect(document.body.textContent).not.toContain("Motorpool reserve:");
  });
});
