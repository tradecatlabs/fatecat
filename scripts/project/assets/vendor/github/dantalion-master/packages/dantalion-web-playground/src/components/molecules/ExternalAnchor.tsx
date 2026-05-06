import { faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons';
import type { ReactNode, VFC } from 'react';
import IconAnchor from './IconAnchor';

/** Type definition of the required attributes. */
export interface Props {
  /** The children items. */
  readonly children?: ReactNode;
  /** The URL. */
  readonly href: string;
  /** Whether the component specifies a “nofflow” flag. */
  readonly nofollow?: boolean;
  /** The tooltip on hover. */
  readonly tooltip?: string;
}

/** The external anchor component */
const ExternalAnchor: VFC<Props> = ({ children, href, nofollow, tooltip }) => (
  <IconAnchor
    href={href}
    icon={faExternalLinkAlt}
    iconClassName="opacity-70 text-xs"
    nofollow={nofollow}
    sup
    tooltip={tooltip}
  >
    {children}
  </IconAnchor>
);
ExternalAnchor.displayName = 'ExternalAnchor';

export default ExternalAnchor;
