import type { Meta, Story } from '@storybook/react';
import ResultFrame, { Props } from './ResultFrame';

export default Object.freeze<Meta>({
  component: ResultFrame,
  title: `atoms/${ResultFrame.displayName}`,
});

const Template: Story<Props> = ({ children }) => (
  <ResultFrame>{children}</ResultFrame>
);

export const Default = Template.bind({});
Default.args = { children: 'Children' };
