import { faTwitter } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { stringify } from 'qs';
import type { ReactNode, VFC } from 'react';
import Anchor from '../atoms/Anchor';

/** Type definition of the required attributes. */
export interface Props {
  /** The children items. */
  readonly children?: ReactNode;
  /** The hashtag. */
  readonly hashtag?: string;
  /** The content. */
  readonly text: string;
  /** URL. */
  readonly url?: string;
}

/**
 * Create the Tweet button URL.
 * @param props The props.
 */
const createUrl = ({ hashtag, text, url }: Omit<Props, 'children'>) =>
  [
    'https://twitter.com/intent/tweet',
    stringify({ button_hashtag: hashtag, url, text }, { addQueryPrefix: true }),
  ].join('');

/** Tweet button component. */
const TweetButton: VFC<Props> = ({ children, ...props }) => (
  <p className="text-center mb-4 select-none">
    <Anchor
      className="block duration-200 ease-in-out flex-grow font-bold leading-5 nm-flat-indigo-100 px-8 py-4 rounded-full text-md sm:text-xl tracking-widest transform transition uppercase dark:nm-flat-purple-800 dark:hover:nm-flat-purple-900 hover:nm-flat-blue-50-lg"
      href={createUrl(props)}
      noblank
      nofollow
    >
      <FontAwesomeIcon className="animate-pulse mx-2" icon={faTwitter} />
      {children}
    </Anchor>
  </p>
);
TweetButton.displayName = 'TweetButton';

export default TweetButton;
