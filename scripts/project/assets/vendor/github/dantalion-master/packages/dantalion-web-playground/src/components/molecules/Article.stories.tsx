import type { Meta, Story } from '@storybook/react';
import Article, { Props } from './Article';

export default Object.freeze<Meta>({
  component: Article,
  title: `molecules/${Article.displayName}`,
});

const Template: Story<Props> = ({
  children,
  featureBody,
  featureHeading,
  tooltipFeatureDetails,
}) => (
  <Article
    featureBody={featureBody}
    featureHeading={featureHeading}
    tooltipFeatureDetails={tooltipFeatureDetails}
  >
    {children}
  </Article>
);

export const Default = Template.bind({});
Default.args = {
  featureBody: ['Foo', 'Bar', 'Qux'],
  children: '_Markdown_ **contents**',
  featureHeading: 'FeatureHeading',
  tooltipFeatureDetails: 'TooltipFeatureDetails',
};
