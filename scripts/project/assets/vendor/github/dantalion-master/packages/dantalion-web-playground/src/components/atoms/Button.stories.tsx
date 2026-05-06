import type { Meta, Story } from '@storybook/react';
import Button, { Props } from './Button';

export default Object.freeze<Meta>({
  argTypes: { onClick: { action: 'clicked' } },
  component: Button,
  title: `atoms/${Button.displayName}`,
});

const Template: Story<Props> = ({ children, className, onClick }) => (
  <Button className={className} onClick={onClick}>
    {children}
  </Button>
);

export const Default = Template.bind({});
Default.args = { className: 'text-4xl', children: 'Children' };
