import type { Meta, Story } from '@storybook/react';
import FooterNavigation, { Props } from './FooterNavigation';

export default Object.freeze<Meta>({
  component: FooterNavigation,
  title: `molecules/${FooterNavigation.displayName}`,
});

const Template: Story<Props> = ({ author }) => (
  <FooterNavigation author={author} />
);

export const Default = Template.bind({});
Default.args = { author: 'Author' };
