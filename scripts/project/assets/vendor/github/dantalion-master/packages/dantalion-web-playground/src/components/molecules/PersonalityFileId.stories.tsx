import type { Meta, Story } from '@storybook/react';
import PersonalityFileId, { Props } from './PersonalityFileId';

export default Object.freeze<Meta>({
  component: PersonalityFileId,
  title: `molecules/${PersonalityFileId.displayName}`,
});

const Template: Story<Props> = ({ caption, children }) => (
  <PersonalityFileId caption={caption}>{children}</PersonalityFileId>
);

export const Default = Template.bind({});
Default.args = { caption: 'Caption', children: 'Children' };
