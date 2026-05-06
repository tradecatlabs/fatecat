import type { ReactNode, VFC } from 'react';
import InlineMarkdownList from './InlineMarkdownList';

/** Type definition of the required attributes. */
export interface Props {
  /** The caption. */
  readonly caption?: ReactNode;
  /** The children items. */
  readonly children?: readonly string[];
  /** The heading level. */
  readonly headingLevel?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
  /** Whether that expand automatically. */
  readonly open?: boolean;
  /** The tooltip on hover. */
  readonly tooltip?: string;
}

/**
 * The collapsable list component which its items allow the Markdown format.
 */
const Details: VFC<Props> = ({
  caption,
  children,
  headingLevel: Heading = 'h4',
  open,
  tooltip,
}) => (
  <details
    className="my-5 nm-flat-gray-200-sm rounded-2xl dark:nm-flat-gray-700-sm md:mx-1 md:rounded-3xl"
    open={open}
  >
    <summary
      className="bg-gray-200 cursor-pointer duration-200 ease-in-out outline-none px-8 py-4 rounded-2xl select-none text-gray-700 text-xl transform transition dark:bg-gray-700 dark:text-gray-200 dark:focus:bg-gray-800 focus:bg-gray-100 dark:hover:bg-gray-800 hover:bg-gray-100 md:rounded-3xl sm:text-2xl"
      tabIndex={0}
      title={tooltip}
    >
      <Heading className="font-bold inline">{caption}</Heading>
    </summary>
    <div className="border-gray-500 border-opacity-50 border-t-2 mx-4 overflow-y-scroll p-2">
      <InlineMarkdownList className="list-disc p-4 md:px-8">
        {children}
      </InlineMarkdownList>
    </div>
  </details>
);
Details.displayName = 'Details';

export default Details;
