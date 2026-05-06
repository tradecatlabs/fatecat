import type { Meta, Story } from '@storybook/react';
import InlineMarkdown, { Props } from './InlineMarkdownList';

export default Object.freeze<Meta>({
  component: InlineMarkdown,
  title: `molecules/${InlineMarkdown.displayName}`,
});

const Template: Story<Props> = ({ children, className, itemType, order }) => (
  <InlineMarkdown className={className} itemType={itemType} order={order}>
    {children}
  </InlineMarkdown>
);

export const Default = Template.bind({});
Default.args = {
  children: ['**Foo**', '_Bar_', 'Qux'],
  className: 'list-disc text-red-900 dark:text-red-200',
  order: false,
};
