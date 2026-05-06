import type { InputHTMLAttributes, ReactNode, VFC } from 'react';

/** Type definition of the required attributes. */
export interface Props
  extends Omit<InputHTMLAttributes<HTMLInputElement>, 'className'> {
  /** The label for control */
  readonly label?: ReactNode;
}

/** The input control component */
const Input: VFC<Props> = ({ id, label, ...props }) => (
  <label
    className="flex flex-col my-4 sm:flex-row sm:items-center"
    htmlFor={id}
  >
    <span className="font-bold mb-1 text-sm tracking-widest text-gray-700 dark:text-gray-200 sm:mb-0 sm:mr-8 sm:w-1/3">
      {label}
    </span>
    <input
      className="appearance-none duration-200 flex-grow leading-5 mr-1 w-full nm-inset-gray-100 px-8 py-4 rounded-full text-gray-800 dark:nm-inset-gray-600 dark:text-gray-100 dark:focus:nm-inset-gray-800 dark:hover:nm-inset-gray-800 focus:nm-inset-gray-50 hover:nm-inset-gray-50 sm:w-2/3"
      id={id}
      tabIndex={0}
      // eslint-disable-next-line react/jsx-props-no-spreading
      {...props}
    />
  </label>
);
Input.displayName = 'Input';

export default Input;
