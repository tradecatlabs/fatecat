import classNames, { Argument } from 'classnames';
import type { ReactNode, VFC } from 'react';

/** Type definition of the required attributes. */
export interface Props {
  /** The children items. */
  readonly children: ReactNode;
  /** If you need the CSS classes, specify them. */
  readonly className?: Argument;
  /** The URL. */
  readonly href: string;
  /** Whether the component remove a target attribute. */
  readonly noblank?: boolean;
  /** Whether the component specifies a “nofflow” flag. */
  readonly nofollow?: boolean;
  /** The tooltip on hover. */
  readonly tooltip?: string;
}

/** The anchor component */
const Anchor: VFC<Props> = ({
  children,
  className,
  href,
  noblank,
  nofollow,
  tooltip,
}) => (
  // eslint-disable-next-line react/jsx-no-target-blank
  <a
    className={classNames(
      'text-blue-800 dark:text-blue-300 dark:hover:text-blue-100 hover:text-blue-500',
      className
    )}
    href={href}
    rel={classNames('noopener noreferrer', { nofollow })}
    tabIndex={0}
    title={tooltip}
    // eslint-disable-next-line react/jsx-props-no-spreading
    {...(noblank ? {} : { target: '_blank' })}
  >
    {children}
  </a>
);
Anchor.displayName = 'Anchor';

export default Anchor;
