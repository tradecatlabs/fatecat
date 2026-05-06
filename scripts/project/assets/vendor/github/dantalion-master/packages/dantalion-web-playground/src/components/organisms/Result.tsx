import type { Detail, Genius, Personality } from '@kurone-kito/dantalion-core';
import { createAccessors } from '@kurone-kito/dantalion-i18n';
import { useMemo, VFC } from 'react';
import { useTranslation } from 'react-i18next';
import AccompanyingResult from './AccompanyingResult';
import GeniusResultDetail from './GeniusResultDetail';
import LifeBaseResultDetail from './LifeBaseResultDetail';
import MotivationResultDetail from './MotivationResultDetail';
import PotentialResultDetail from './PotentialResultDetail';
import PersonalityFileId from './PersonalityFileId';
import SubGeniusResultDetail from './SubGeniusResultDetail';
import TweetButton from './TweetButton';
import VectorResultDetail from './VectorResultDetail';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the details for personality. */
  readonly detail: Detail;
  /** Specifies the inner personality type. */
  readonly inner: Genius;
  /** Specifies the nickname. */
  readonly nickname?: string;
  /** Specifies the details for Personality. */
  readonly personality?: Personality;
}

/** The result component. */
const Result: VFC<Props> = ({ detail, inner, nickname, personality }) => {
  const { t } = useTranslation();
  const accessors = useMemo(() => createAccessors(t), [t]);
  const descriptions = accessors.getDescription();
  const geniusDetails = accessors.genius.getCategoryDetail();
  const innerDetail = accessors.genius.getByKey(inner);
  return !personality || personality.inner === inner ? (
    <>
      <article>
        <VectorResultDetail
          accessor={accessors.vector}
          nickname={nickname}
          strategy={descriptions.strategy}
          vector={detail.vector}
        />
        <GeniusResultDetail
          descriptions={descriptions}
          details={geniusDetails}
          inner={innerDetail}
          nickname={nickname}
        >
          {!!personality && (
            <SubGeniusResultDetail
              descriptions={descriptions}
              details={geniusDetails.descriptions}
              inner={innerDetail}
              outer={accessors.genius.getByKey(personality.outer)}
              workStyle={accessors.genius.getByKey(personality.workStyle)}
            />
          )}
        </GeniusResultDetail>
        {!!personality && (
          <>
            <LifeBaseResultDetail
              accessors={accessors.lifeBase}
              lifeBase={personality.lifeBase}
              nickname={nickname}
            />
            <PotentialResultDetail
              accessors={accessors.potential}
              potentials={personality.potentials}
              nickname={nickname}
            />
          </>
        )}
        <MotivationResultDetail
          accessors={accessors.motivation}
          motivation={detail.motivation}
        />
        <AccompanyingResult
          accessors={accessors}
          details={detail}
          nickname={nickname}
        />
        {!!personality && <PersonalityFileId personality={personality} />}
      </article>
      <aside>
        <TweetButton nickname={nickname} hooks={innerDetail.summary} />
      </aside>
    </>
  ) : null;
};
Result.displayName = 'Result';

export default Result;
