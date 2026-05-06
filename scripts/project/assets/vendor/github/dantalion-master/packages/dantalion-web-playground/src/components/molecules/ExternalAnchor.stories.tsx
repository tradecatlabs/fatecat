import type { Meta, Story } from '@storybook/react';
import ExternalAnchor, { Props } from './ExternalAnchor';

export default Object.freeze<Meta>({
  component: ExternalAnchor,
  title: `molecules/${ExternalAnchor.displayName}`,
});

const Template: Story<Props> = ({ children, href, nofollow, tooltip }) => (
  <ExternalAnchor href={href} nofollow={nofollow} tooltip={tooltip}>
    {children}
  </ExternalAnchor>
);

export const Default = Template.bind({});
Default.args = {
  children: 'Dantalion',
  href: 'https://kurone-kito.github.io/dantalion',
  nofollow: false,
  tooltip: 'Tooltip',
};
