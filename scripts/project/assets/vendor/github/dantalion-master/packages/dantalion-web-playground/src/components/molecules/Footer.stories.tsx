import type { Meta, Story } from '@storybook/react';
import Footer, { Props } from './Footer';

export default Object.freeze<Meta>({
  component: Footer,
  title: `molecules/${Footer.displayName}`,
});

const Template: Story<Props> = ({ author, children }) => (
  <Footer author={author}>{children}</Footer>
);

export const Default = Template.bind({});
Default.args = { author: 'Author', children: ['Children'] };
