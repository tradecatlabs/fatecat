import type { Motivation } from '@kurone-kito/dantalion-core';
import type { DetailAccessor } from '@kurone-kito/dantalion-i18n';
import type { VFC } from 'react';
import ResultFrame from '../atoms/ResultFrame';
import TupleList from '../molecules/TupleList';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the accessor object */
  readonly accessors: DetailAccessor<string, Motivation, string>;
  /** Specifies the motivation value */
  readonly motivation: Motivation;
}

/** The result component. */
const MotivationResultDetail: VFC<Props> = ({ accessors, motivation }) => (
  <ResultFrame>
    <TupleList className="list-disc pl-8">
      {[[accessors.getCategoryDetail(), accessors.getByKey(motivation)]]}
    </TupleList>
  </ResultFrame>
);
MotivationResultDetail.displayName = 'MotivationResultDetail';

export default MotivationResultDetail;
