import type { Meta, Story } from '@storybook/react';
import ResultHeading, { Props } from './ResultHeading';

export default Object.freeze<Meta>({
  component: ResultHeading,
  title: `atoms/${ResultHeading.displayName}`,
});

const Template: Story<Props> = ({ additional, children, detail, heading }) => (
  <ResultHeading additional={additional} detail={detail} heading={heading}>
    {children}
  </ResultHeading>
);

export const Default = Template.bind({});
Default.args = {
  additional: 'Additional',
  children: 'Children',
  detail: 'Detail',
  heading: 'Heading',
};
