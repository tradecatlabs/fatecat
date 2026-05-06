import type { Meta, Story } from '@storybook/react';
import Anchor, { Props } from './Anchor';

export default Object.freeze<Meta>({
  component: Anchor,
  title: `atoms/${Anchor.displayName}`,
});

const Template: Story<Props> = ({
  children,
  className,
  href,
  noblank,
  nofollow,
  tooltip,
}) => (
  <Anchor
    className={className}
    href={href}
    noblank={noblank}
    nofollow={nofollow}
    tooltip={tooltip}
  >
    {children}
  </Anchor>
);

export const Default = Template.bind({});
Default.args = {
  className: 'text-4xl',
  href: 'https://kurone-kito.github.io/dantalion',
  children: 'Dantalion',
  noblank: false,
  nofollow: false,
  tooltip: 'Tooltip',
};
