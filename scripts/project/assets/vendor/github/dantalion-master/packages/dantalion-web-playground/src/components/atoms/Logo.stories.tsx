import type { Meta, Story } from '@storybook/react';
import Logo from './Logo';

export default Object.freeze<Meta>({
  component: Logo,
  title: `atoms/${Logo.displayName}`,
});

const Template: Story = () => <Logo />;

export const Default = Template.bind({});
Default.args = {};
