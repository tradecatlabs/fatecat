import type { IconProp } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import type { ReactNode, VFC } from 'react';
import Anchor from '../atoms/Anchor';

/** Type definition of the required attributes. */
export interface Props {
  /** The children items. */
  readonly children?: ReactNode;
  /** The URL. */
  readonly href: string;
  /** The icon. */
  readonly icon: IconProp;
  /** If you need the CSS classes for icon, specify them. */
  readonly iconClassName?: string;
  /** Whether the component specifies a “nofflow” flag. */
  readonly nofollow?: boolean;
  /** Whether the icon specifies as a superscript. */
  readonly sup?: boolean;
  /** The tooltip on hover. */
  readonly tooltip?: string;
}

/** The footer component */
const IconAnchor: VFC<Props> = ({
  children,
  href,
  icon,
  iconClassName,
  nofollow,
  sup,
  tooltip,
}) => {
  const Sup = sup ? 'sup' : 'span';
  return (
    <Anchor href={href} nofollow={nofollow} tooltip={tooltip}>
      {children && <span className="mr-1">{children}</span>}
      <Sup>
        <FontAwesomeIcon icon={icon} className={iconClassName} />
      </Sup>
    </Anchor>
  );
};
IconAnchor.displayName = 'IconAnchor';

export default IconAnchor;
