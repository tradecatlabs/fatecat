import type { LifeBase } from '@kurone-kito/dantalion-core';
import type {
  DetailAccessor,
  DetailsBaseType,
} from '@kurone-kito/dantalion-i18n';
import type { VFC } from 'react';
import { useTranslation } from 'react-i18next';
import ResultDetail from '../molecules/ResultDetail';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the accessor object */
  readonly accessors: DetailAccessor<
    DetailsBaseType<string[]>,
    LifeBase,
    string
  >;
  /** Specifies the lifebase value */
  readonly lifeBase: LifeBase;
  /** Specifies the nickname. */
  readonly nickname?: string;
}

/** The result component. */
const LifeBaseResultDetail: VFC<Props> = ({
  accessors,
  lifeBase,
  nickname,
}) => {
  const { t } = useTranslation();
  const { detail, name } = accessors.getByKey(lifeBase);
  const desc = t<string, DetailsBaseType>('web.result.lifeBase', {
    nickname,
    returnObjects: true,
  });
  return (
    <ResultDetail
      heading={accessors.getCategoryDetail()}
      headingDetail={desc.detail}
      hook={desc.name}
      hookAdditional={name}
      moreDetail={detail}
    />
  );
};
LifeBaseResultDetail.displayName = 'LifeBaseResultDetail';

export default LifeBaseResultDetail;
