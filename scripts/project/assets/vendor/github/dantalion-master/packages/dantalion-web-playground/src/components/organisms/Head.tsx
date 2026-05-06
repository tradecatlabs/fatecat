import NextHead from 'next/head';
import { useTranslation } from 'react-i18next';
import { VFC } from 'react';
import Title from '../atoms/head/Title';
import HeadContents from '../molecules/HeadContents';

/** The web app name. */
const appName = 'Dantalion';

/** Type definition of the required attributes. */
export interface Props {
  /** Whether the icon specifies as a superscript. */
  readonly pageName?: string;
}

const Head: VFC<Props> = ({ pageName }) => {
  const { t } = useTranslation();
  return (
    <>
      <Title appName={appName} pageName={pageName} />
      <NextHead>
        <HeadContents
          baseUrl={process.env.assetPrefix}
          author={`${t('web.author')}, @kurone_kito`}
          appName={appName}
          article={!!pageName}
          bannerHeight={630}
          bannerPath="/favicons/ogp.png"
          bannerWidth={1200}
          color="#E5E7EB"
          description={t('web.description')}
          keywords={[
            'ba-zi',
            'bazi',
            'birthday',
            'cancode',
            'chinese-astrology',
            'divination',
            'four-pillars',
            'library',
            'self-assessment',
            'ziweidoushu',
            'zodiac',
            '占い',
            '自己分析',
            '誕生日',
          ]}
          pageName={pageName}
        />
      </NextHead>
    </>
  );
};
Head.displayName = 'Head';

export default Head;
