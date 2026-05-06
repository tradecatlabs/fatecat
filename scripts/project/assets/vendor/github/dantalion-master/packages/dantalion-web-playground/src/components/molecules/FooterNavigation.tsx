import {
  faGithub,
  faTwitter,
  faYoutube,
} from '@fortawesome/free-brands-svg-icons';
import { faHome } from '@fortawesome/free-solid-svg-icons';
import classNames from 'classnames';
import type { ReactNode, VFC } from 'react';
import List from '../atoms/List';
import IconAnchor from './IconAnchor';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the author-name */
  readonly author?: ReactNode;
}

/** The footer component */
const FooterNavigation: VFC<Props> = ({ author }) => (
  <List
    className="divide-x-2 divide-gray-500 divide-opacity-50 flex flex-row justify-center p-4"
    itemType={({ className, ...props }) => (
      <li
        className={classNames('place-self-center px-3', className)}
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...props}
      />
    )}
  >
    <>&copy; {author}</>
    <IconAnchor
      href="https://twitter.com/kurone_kito"
      icon={faTwitter}
      tooltip="Twitter"
    />
    <IconAnchor
      href="https://github.com/kurone-kito"
      icon={faGithub}
      tooltip="GitHub"
    />
    <IconAnchor
      href="https://www.youtube.com/channel/UCJs_ejHQM0rcemJaeO2s5vA"
      icon={faYoutube}
      tooltip="YouTube"
    />
    <IconAnchor href="https://kit.black/" icon={faHome} tooltip="Homepage" />
  </List>
);
FooterNavigation.displayName = 'FooterNavigation';

export default FooterNavigation;
