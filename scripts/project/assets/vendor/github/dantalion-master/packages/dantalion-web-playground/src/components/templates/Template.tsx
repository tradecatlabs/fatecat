import { Genius, getDetail } from '@kurone-kito/dantalion-core';
import { createAccessors } from '@kurone-kito/dantalion-i18n';
import { useTranslation } from 'react-i18next';
import { useMemo, VFC } from 'react';
import ReactMarkdown from 'react-markdown';
import Anchor from '../atoms/Anchor';
import Header from '../atoms/Header';
import Article from '../molecules/Article';
import Footer from '../molecules/Footer';
import BirthForm from '../organisms/BirthForm';
import Head from '../organisms/Head';
import AppearanceSelector from '../organisms/AppearanceSelector';
import LanguageSelector from '../organisms/LanguageSelector';
import Result from '../organisms/Result';
import { usePSDecoder } from '../../hooks/usePersonality';
import FormReducer from '../../stores/FormReducer';

/** Type definition of the required attributes. */
export interface Props {
  readonly inner?: Genius;
}

const Template: VFC<Props> = ({ inner }) => {
  const { t } = useTranslation();
  const accessors = useMemo(() => createAccessors(t), [t]);
  const [ps, nickname] = usePSDecoder();
  const concreteInner = ps?.inner ?? inner;
  const dt = concreteInner && getDetail(concreteInner);
  const pageName =
    concreteInner && accessors.genius.getByKey(concreteInner).summary;
  return (
    <>
      <Head pageName={pageName} />
      <Header>
        {ps ? t('web.result.heading', { nickname }) : t('web.description')}
      </Header>
      <main className="md:container mx-auto text-gray-600">
        {!!(concreteInner && dt) && (
          <Result
            detail={dt}
            inner={concreteInner}
            nickname={nickname}
            personality={ps}
          />
        )}
        <FormReducer.Provider>
          <BirthForm />
        </FormReducer.Provider>
        <Article
          featureBody={t('web.feature.body', { returnObjects: true })}
          featureHeading={t('web.feature.title')}
          tooltipFeatureDetails={t('web.tooltip.summary')}
        >
          {t('web.preface', { joinArrays: '\n\n' })}
        </Article>
        <ReactMarkdown className="mx-0 my-5 nm-inset-gray-500-sm overflow-auto p-6 text-white dark:nm-inset-gray-800-sm dark:text-gray-200 md:rounded-3xl">
          {t('web.install', { joinArrays: '\n' })}
        </ReactMarkdown>
        <p className="font-bold text-center text-xl py-6">
          <Anchor href="https://github.com/kurone-kito/dantalion">
            {t('web.seeRepo')}
          </Anchor>
        </p>
      </main>
      <Footer author={t('web.author')}>
        <LanguageSelector />
        <AppearanceSelector />
      </Footer>
    </>
  );
};
Template.displayName = 'Template';

export default Template;
