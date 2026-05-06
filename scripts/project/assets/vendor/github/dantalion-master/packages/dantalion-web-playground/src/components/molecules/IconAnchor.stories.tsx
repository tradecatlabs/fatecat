import { faCat } from '@fortawesome/free-solid-svg-icons';
import type { Meta, Story } from '@storybook/react';
import IconAnchor, { Props } from './IconAnchor';

export default Object.freeze<Meta>({
  component: IconAnchor,
  title: `molecules/${IconAnchor.displayName}`,
});

const Template: Story<Props> = ({
  children,
  href,
  icon,
  iconClassName,
  nofollow,
  sup,
  tooltip,
}) => (
  <IconAnchor
    href={href}
    icon={icon}
    iconClassName={iconClassName}
    nofollow={nofollow}
    sup={sup}
    tooltip={tooltip}
  >
    {children}
  </IconAnchor>
);

export const Default = Template.bind({});
Default.args = {
  children: 'Dantalion',
  href: 'https://kurone-kito.github.io/dantalion',
  icon: faCat,
  iconClassName: 'text-6xl',
  nofollow: false,
  sup: false,
  tooltip: 'Tooltip',
};
