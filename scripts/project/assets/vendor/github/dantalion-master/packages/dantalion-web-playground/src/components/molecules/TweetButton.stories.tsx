import type { Meta, Story } from '@storybook/react';
import TweetButton, { Props } from './TweetButton';

export default Object.freeze<Meta>({
  component: TweetButton,
  title: `molecules/${TweetButton.displayName}`,
});

const Template: Story<Props> = ({ children, hashtag, text, url }) => (
  <TweetButton hashtag={hashtag} text={text} url={url}>
    {children}
  </TweetButton>
);

export const Default = Template.bind({});
Default.args = {
  children: 'Tweet',
  hashtag: 'DantalionPD',
  text: 'Dantalion: Calculates the personality from the birthday.',
  url: 'https://kurone-kito.github.io/dantalion',
};
