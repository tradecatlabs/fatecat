import type { Potential } from '@kurone-kito/dantalion-core';
import type { DetailAccessor } from '@kurone-kito/dantalion-i18n';
import type { VFC } from 'react';
import { useTranslation } from 'react-i18next';
import ResultDetail from '../molecules/ResultDetail';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the accessor object */
  readonly accessors: DetailAccessor<
    readonly string[],
    readonly [Potential, Potential]
  >;
  /** Specifies the lifebase value */
  readonly potentials: readonly [Potential, Potential];
  /** Specifies the nickname. */
  readonly nickname?: string;
}

/** The result component. */
const LifeBaseResultDetail: VFC<Props> = ({
  accessors,
  potentials,
  nickname,
}) => {
  const { t } = useTranslation();
  const desc = accessors.getCategoryDetail();
  return (
    <ResultDetail
      heading={desc.name}
      headingDetail={desc.detail}
      hook={t('web.result.potential', { nickname })}
      moreDetail={accessors.getByKey(potentials)}
    />
  );
};
LifeBaseResultDetail.displayName = 'LifeBaseResultDetail';

export default LifeBaseResultDetail;
