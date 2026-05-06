import type { Meta, Story } from '@storybook/react';
import List, { Props } from './List';

export default Object.freeze<Meta>({
  component: List,
  title: `atoms/${List.displayName}`,
});

const Template: Story<Props> = ({ children, className, itemType, order }) => (
  <List className={className} itemType={itemType} order={order}>
    {children}
  </List>
);

export const Default = Template.bind({});
Default.args = {
  children: ['A', 'B', 'C'],
  className: 'list-disc text-red-900 dark:text-red-300',
  order: false,
};
