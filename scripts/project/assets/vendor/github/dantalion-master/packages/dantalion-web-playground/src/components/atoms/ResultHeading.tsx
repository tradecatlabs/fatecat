import type { ReactNode, VFC } from 'react';
import InlineMarkdown from './InlineMarkdown';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the additional information. */
  readonly additional?: ReactNode;
  /** The children items. */
  readonly children?: ReactNode;
  /** Specifies the detail. */
  readonly detail?: string;
  /** Specifies the heading. */
  readonly heading?: ReactNode;
}

/** The heading for result */
const ResultHeading: VFC<Props> = ({
  additional,
  children,
  detail = '',
  heading,
}) => (
  <header className="leading-loose mb-4">
    <div className="divide-x divide-gray-500 divide-opacity-50 flex">
      <h2 className="flex-grow-0 pr-4 text-gray-900 dark:text-gray-100">
        {heading}
      </h2>
      <p className="flex-grow pl-4">
        <InlineMarkdown>{detail}</InlineMarkdown>
      </p>
    </div>
    <hr className="border-gray-500 border-opacity-50 mb-6 mt-3" />
    <div className="p-0 text-2xl text-center text-gray-700 dark:text-gray-200 sm:text-3xl">
      <h3 className="font-extrabold p-0">{children}</h3>
      {!!additional && <p className="font-extralight p-0">{additional}</p>}
    </div>
  </header>
);
ResultHeading.displayName = 'ResultHeading';

export default ResultHeading;
