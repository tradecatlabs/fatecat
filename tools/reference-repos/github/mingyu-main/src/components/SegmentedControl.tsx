type SegmentedOption<T extends string | number | boolean> = {
  label: string;
  value: T;
};

type SegmentedControlProps<T extends string | number | boolean> = {
  value: T;
  options: Array<SegmentedOption<T>>;
  onChange: (value: T) => void;
};

export function SegmentedControl<T extends string | number | boolean>(
  props: SegmentedControlProps<T>,
) {
  const { value, options, onChange } = props;
  const activeIndex = Math.max(
    0,
    options.findIndex((option) => option.value === value),
  );
  const width = `${100 / options.length}%`;
  const left = `${(100 / options.length) * activeIndex}%`;

  return (
    <div className="segmented-control-react">
      <div
        className="segmented-control-indicator"
        style={{
          width,
          left,
        }}
      />
      {options.map((option) => (
        <button
          key={String(option.value)}
          type="button"
          className={`segmented-control-item-react ${value === option.value ? 'active' : ''}`}
          onClick={() => onChange(option.value)}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}
