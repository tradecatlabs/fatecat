import type { Meta, Story } from '@storybook/react';
import Select, { Props } from './Select';

export default Object.freeze<Meta>({
  argTypes: { onChange: { action: 'changed' } },
  component: Select,
  title: `atoms/${Select.displayName}`,
});

const Template: Story<Props> = ({
  defaultValue,
  id,
  label,
  onChange,
  source,
}) => (
  <Select
    defaultValue={defaultValue}
    id={id}
    label={label}
    onChange={onChange}
    source={source}
  />
);

export const Default = Template.bind({});
Default.args = {
  defaultValue: 'baz',
  id: 'id',
  label: 'Label',
  source: ['foo', 'bar', ['baz', 'qux']],
};
