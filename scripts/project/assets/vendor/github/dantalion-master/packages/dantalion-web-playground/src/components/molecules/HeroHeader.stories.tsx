import type { Meta, Story } from '@storybook/react';
import HeroHeader, { Props } from './HeroHeader';

export default Object.freeze<Meta>({
  component: HeroHeader,
  title: `molecules/${HeroHeader.displayName}`,
});

const Template: Story<Props> = () => <HeroHeader />;

export const Default = Template.bind({});
Default.args = {};
