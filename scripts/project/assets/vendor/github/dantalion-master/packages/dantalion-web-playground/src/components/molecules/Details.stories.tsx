import type { Meta, Story } from '@storybook/react';
import Details, { Props } from './Details';

export default Object.freeze<Meta>({
  component: Details,
  title: `molecules/${Details.displayName}`,
});

const Template: Story<Props> = ({
  caption,
  children,
  headingLevel,
  open,
  tooltip,
}) => (
  <Details
    caption={caption}
    headingLevel={headingLevel}
    open={open}
    tooltip={tooltip}
  >
    {children}
  </Details>
);

export const Default = Template.bind({});
Default.args = {
  caption: 'FeatureHeading',
  children: ['Foo', 'Bar', 'Qux'],
  headingLevel: 'h1',
  open: true,
  tooltip: 'Tooltip',
};
