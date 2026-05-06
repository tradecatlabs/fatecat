import type { Meta, Story } from '@storybook/react';
import Header, { Props } from './Header';

export default Object.freeze<Meta>({
  component: Header,
  title: `atoms/${Header.displayName}`,
});

const Template: Story<Props> = ({ children }) => <Header>{children}</Header>;

export const Default = Template.bind({});
Default.args = { children: 'Children' };
