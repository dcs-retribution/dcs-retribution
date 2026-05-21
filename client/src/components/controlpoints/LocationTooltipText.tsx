import SplitLines from "../splitlines/SplitLines";

interface LocationTooltipTextProps {
  name: string;
  units?: string[];
}

export const LocationTooltipText = (props: LocationTooltipTextProps) => {
  return (
    <>
      <h3 style={{ margin: 0 }}>{props.name}</h3>
      {props.units && props.units.length > 0 && (
        <SplitLines items={props.units} />
      )}
    </>
  );
};

export default LocationTooltipText;
