import type { Meta, Story } from '@storybook/react';
import Input, { Props } from './Input';

export default Object.freeze<Meta>({
  argTypes: { onBlur: { action: 'blured' }, onChange: { action: 'changed' } },
  component: Input,
  title: `atoms/${Input.displayName}`,
});

const Template: Story<Props> = ({ label }) => <Input label={label} />;

export const Default = Template.bind({});
Default.args = { label: 'Label', placeholder: 'Placeholder' };
