import classNames, { Argument } from 'classnames';
import type { MouseEventHandler, ReactNode, VFC } from 'react';

/** Type definition of the required attributes. */
export interface Props {
  /** The children items */
  readonly children?: ReactNode;
  /** If you need the CSS classes, specify them */
  readonly className?: Argument;
  /** Callback to call when the user taps */
  readonly onClick?: MouseEventHandler<HTMLButtonElement>;
}

/** The button component */
const Button: VFC<Props> = ({ children, className, onClick }) => (
  <div className={classNames('flex justify-center pt-8', className)}>
    <button
      className="duration-200 ease-in-out flex-grow font-bold leading-5 nm-flat-gray-300 px-8 py-4 rounded-full text-gray-800 tracking-widest transform transition uppercase dark:nm-flat-gray-600 dark:text-gray-300 dark:hover:nm-flat-gray-800-lg dark:hover:text-gray-100 hover:nm-flat-gray-50-lg hover:text-gray-900"
      onClick={onClick}
      tabIndex={0}
      type="submit"
    >
      {children}
    </button>
  </div>
);
Button.displayName = 'Button';

export default Button;
