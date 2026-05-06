import type {
  DesctiptionsType,
  PersonalityDetailBaseType,
  PersonalityType,
} from '@kurone-kito/dantalion-i18n';
import { useMemo, VFC } from 'react';
import { useTranslation } from 'react-i18next';
import ReactMarkdown from 'react-markdown';
import InlineMarkdownList from '../molecules/InlineMarkdownList';

/** Type definition of the required attributes. */
export interface Props {
  /** The resources of the descriptions. */
  readonly descriptions: Pick<DesctiptionsType, 'genius1' | 'genius2'>;
  /** The resources of the personality details. */
  readonly details: PersonalityDetailBaseType;
  /** The resources of the inner personality details. */
  readonly inner: Pick<PersonalityType, 'name' | 'summary'>;
  /** The resources of the outer personality details. */
  readonly outer: Pick<PersonalityType, 'name' | 'summary'>;
  /** The resources of the workStyle personality details. */
  readonly workStyle: Pick<PersonalityType, 'name' | 'summary'>;
}

/** Create the source from props. */
const createSource = ({
  inner,
  outer,
  workStyle,
}: Pick<Props, 'inner' | 'outer' | 'workStyle'>) =>
  (
    [
      ['inner', inner],
      ['outer', outer],
      ['workStyle', workStyle],
    ] as const
  ).map<readonly [string, string]>(([key, { summary, name }]) => [
    `web.result.genius.${key}`,
    `${summary} ... **${name}**`,
  ]);

/** The result component. */
const SubGeniusResultDetail: VFC<Props> = ({
  descriptions,
  details,
  inner,
  outer,
  workStyle,
}) => {
  const { t } = useTranslation();
  const source = useMemo(
    () =>
      createSource({ inner, outer, workStyle }).map(([key, type]) =>
        t(key, { type })
      ),
    [inner, outer, t, workStyle]
  );
  return (
    <>
      <hr className="border-gray-300 my-3" />
      <ReactMarkdown>{descriptions.genius1}</ReactMarkdown>
      <InlineMarkdownList className="list-decimal p-4 md:px-8" order>
        {Object.values(details)}
      </InlineMarkdownList>
      <ReactMarkdown>{descriptions.genius2}</ReactMarkdown>
      <InlineMarkdownList className="list-decimal p-4 md:px-8" order>
        {source}
      </InlineMarkdownList>
    </>
  );
};
SubGeniusResultDetail.displayName = 'SubGeniusResultDetail';

export default SubGeniusResultDetail;
