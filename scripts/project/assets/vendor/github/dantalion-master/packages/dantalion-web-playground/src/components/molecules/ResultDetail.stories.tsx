import type { Meta, Story } from '@storybook/react';
import ResultDetail, { Props } from './ResultDetail';

export default Object.freeze<Meta>({
  component: ResultDetail,
  title: `molecules/${ResultDetail.displayName}`,
});

const Template: Story<Props> = ({
  children,
  heading,
  headingDetail,
  hook,
  hookAdditional,
  moreDetail,
}) => (
  <ResultDetail
    heading={heading}
    headingDetail={headingDetail}
    hook={hook}
    hookAdditional={hookAdditional}
    moreDetail={moreDetail}
  >
    {children}
  </ResultDetail>
);

export const Default = Template.bind({});
Default.args = {
  children: 'Dantalion',
  heading: 'Heading',
  headingDetail: 'HeadingDetail',
  hook: 'Hook',
  hookAdditional: 'HookAdditional',
  moreDetail: ['Foo', 'Bar', 'Qux'],
};
