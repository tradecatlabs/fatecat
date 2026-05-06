import type {
  DesctiptionsType,
  DetailsBaseType,
  PersonalityType,
} from '@kurone-kito/dantalion-i18n';
import type { ReactNode, VFC } from 'react';
import { useTranslation } from 'react-i18next';
import Details from '../molecules/Details';
import ResultDetail from '../molecules/ResultDetail';

/** Type definition of the required attributes. */
export interface Props {
  /** The children items */
  readonly children?: ReactNode;
  /** The resources of the descriptions. */
  readonly descriptions: Pick<DesctiptionsType, 'strategy' | 'weak'>;
  /** The resources of the personality details. */
  readonly details: DetailsBaseType;
  /** The resources of the inner personality details. */
  readonly inner: PersonalityType;
  /** Specifies the nickname. */
  readonly nickname?: string;
}

/** The result component. */
const GeniusResultDetail: VFC<Props> = ({
  children,
  descriptions,
  details,
  inner,
  nickname,
}) => {
  const { t } = useTranslation();
  return (
    <ResultDetail
      heading={details.name}
      headingDetail={details.detail}
      hook={
        <>
          {inner.summary}
          <br />
          {t('web.result.probed', { nickname, type: inner.name })}
        </>
      }
      moreDetail={inner.detail}
    >
      <Details caption={descriptions.weak} tooltip={t('web.tooltip.summary')}>
        {inner.weak}
      </Details>
      <Details
        caption={descriptions.strategy}
        tooltip={t('web.tooltip.summary')}
      >
        {inner.strategy}
      </Details>
      {children}
    </ResultDetail>
  );
};
GeniusResultDetail.displayName = 'GeniusResultDetail';

export default GeniusResultDetail;
