import type { Meta, Story } from '@storybook/react';
import TupleList, { Props } from './TupleList';

export default Object.freeze<Meta>({
  component: TupleList,
  title: `molecules/${TupleList.displayName}`,
});

const Template: Story<Props> = ({ children, className, itemType, order }) => (
  <TupleList className={className} itemType={itemType} order={order}>
    {children}
  </TupleList>
);

export const Default = Template.bind({});
Default.args = {
  children: [
    ['Foo', 'Hoge'],
    ['Bar', 'Fuga'],
    ['Qux', 'Piyo'],
  ],
  className: 'list-disc text-red-900 dark:text-red-200',
  order: false,
};
