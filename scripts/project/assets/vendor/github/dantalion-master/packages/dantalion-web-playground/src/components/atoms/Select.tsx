import type { ChangeEventHandler, ReactNode, VFC } from 'react';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the default value. */
  readonly defaultValue?: string;
  /** Specifies the ID. */
  readonly id: string;
  /** Specifies the label. */
  readonly label?: ReactNode;
  /** Callback to call when the user changes the control. */
  readonly onChange?: ChangeEventHandler<HTMLSelectElement>;
  /** Specifies the source. */
  readonly source?: readonly (readonly [string, string] | string)[];
}

/** The select component. */
const Select: VFC<Props> = ({ defaultValue, id, label, onChange, source }) => (
  <label className="flex flex-col sm:flex-row sm:items-center" htmlFor={id}>
    <span className="font-bold mb-1 text-sm tracking-widest text-gray-700 dark:text-gray-200 sm:mb-0 sm:mr-8 sm:w-1/4">
      {label}
    </span>
    <div className="rounded-full duration-200 nm-flat-gray-200 flex-grow dark:nm-flat-gray-600  dark:hover:nm-flat-gray-800 hover:nm-flat-gray-50 sm:w-3/4">
      <select
        className="appearance-none w-full px-8 py-4 bg-transparent font-semibold text-gray-800 dark:text-gray-100"
        defaultValue={defaultValue}
        disabled={!source?.length}
        id={id}
        name={id}
        onChange={onChange}
        tabIndex={0}
      >
        {source?.map((item) => {
          const [value, text] = typeof item === 'string' ? [item, item] : item;
          return (
            <option key={value} value={value}>
              {text}
            </option>
          );
        })}
      </select>
    </div>
  </label>
);
Select.displayName = 'Select';

export default Select;
