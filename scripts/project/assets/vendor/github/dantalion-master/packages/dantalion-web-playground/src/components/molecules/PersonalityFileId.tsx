import type { ReactNode, VFC } from 'react';
import InlineMarkdown from '../atoms/InlineMarkdown';
import ResultFrame from '../atoms/ResultFrame';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the heading. */
  readonly caption?: ReactNode;
  /** The children items. */
  readonly children?: string;
}

/** The personality file component */
const PersonalityFileId: VFC<Props> = ({ caption, children }) => (
  <ResultFrame>
    {caption}:&nbsp;<InlineMarkdown>{`\`${children}\``}</InlineMarkdown>
  </ResultFrame>
);
PersonalityFileId.displayName = 'PersonalityFileId';

export default PersonalityFileId;
