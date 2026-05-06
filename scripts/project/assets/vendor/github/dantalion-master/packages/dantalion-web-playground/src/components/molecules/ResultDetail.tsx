import type { ReactNode, VFC } from 'react';
import ResultFrame from '../atoms/ResultFrame';
import ResultHeading from '../atoms/ResultHeading';
import InlineMarkdownList from './InlineMarkdownList';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the main content */
  readonly children?: ReactNode;
  /** Specifies the heading */
  readonly heading?: ReactNode;
  /** Specifies the detail of heading */
  readonly headingDetail?: string;
  /** Specifies the hook text */
  readonly hook?: ReactNode;
  /** Specifies the additional hook text */
  readonly hookAdditional?: ReactNode;
  /** Specifies the more detail */
  readonly moreDetail?: readonly string[];
}

/** The detail of result */
const ResultDetail: VFC<Props> = ({
  children,
  heading,
  headingDetail,
  hook,
  hookAdditional,
  moreDetail,
}) => (
  <ResultFrame>
    <ResultHeading
      additional={hookAdditional}
      detail={headingDetail}
      heading={heading}
    >
      {hook}
    </ResultHeading>
    <InlineMarkdownList className="leading-loose list-disc p-4 md:px-8">
      {moreDetail}
    </InlineMarkdownList>
    {children}
  </ResultFrame>
);
ResultDetail.displayName = 'ResultDetail';

export default ResultDetail;
