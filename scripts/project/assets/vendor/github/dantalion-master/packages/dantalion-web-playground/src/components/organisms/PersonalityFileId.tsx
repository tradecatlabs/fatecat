import { Personality, toCC } from '@kurone-kito/dantalion-core';
import type { VFC } from 'react';
import { useTranslation } from 'react-i18next';
import MoleculesPersonalityFileId from '../molecules/PersonalityFileId';

/** Type definition of the required attributes. */
export interface Props {
  /** The details for Personality. */
  readonly personality: Personality;
}

/** The personality file component */
const PersonalityFileId: VFC<Props> = ({ personality }) => {
  const { t } = useTranslation();
  return (
    <MoleculesPersonalityFileId caption={t('web.result.profile')}>
      {toCC(personality)}
    </MoleculesPersonalityFileId>
  );
};
PersonalityFileId.displayName = 'PersonalityFileId';

export default PersonalityFileId;
