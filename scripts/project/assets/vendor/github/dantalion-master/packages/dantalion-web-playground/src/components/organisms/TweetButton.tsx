import type { VFC } from 'react';
import { useTranslation } from 'react-i18next';
import useIsSsr from '../../hooks/useIsSsr';
import MoleculesTweetButton from '../molecules/TweetButton';

/** Type definition of the required attributes. */
export interface Props {
  /** The hook text. */
  readonly hooks?: string;
  /** Specifies the nickname. */
  readonly nickname?: string;
}

/** Tweet button component. */
const TweetButton: VFC<Props> = ({ hooks, nickname }) => {
  const { t } = useTranslation();
  const isSsr = useIsSsr();
  return (
    <MoleculesTweetButton
      hashtag={t('web.share.hashtag')}
      text={[t('web.result.heading', { nickname }), hooks].join('\n')}
      url={isSsr() ? undefined : window.location.href}
    >
      {t('web.share.tweet')}
    </MoleculesTweetButton>
  );
};
TweetButton.displayName = 'TweetButton';

export default TweetButton;
