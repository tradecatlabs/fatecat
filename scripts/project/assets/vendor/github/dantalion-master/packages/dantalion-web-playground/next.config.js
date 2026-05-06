const { withSentryConfig } = require('@sentry/nextjs');

const localDomain = '';
const productDomain = 'https://kurone-kito.github.io';
const productPath = '/dantalion';
const isProd = process.env.NODE_ENV === 'production';
const isCI = !!process.env.CI;
const path = !isCI && isProd ? '' : productPath;
const assetPrefix = (isCI && isProd ? productDomain : localDomain) + path;
const applyDarkMode = `
const { classList } = window.document.getElementsByTagName('html')[0];
localStorage.theme === 'dark' ||
(!('theme' in localStorage) &&
  window.matchMedia('(prefers-color-scheme: dark)').matches)
  ? classList.add('dark')
  : classList.remove('dark');
`;

/** @type {Partial<import('next/dist/next-server/server/config-shared').NextConfig>} */
const providedExports = {
  assetPrefix,
  basePath: path,
  env: { applyDarkMode, assetPrefix },
  future: { strictPostcssConfiguration: true },
  // i18n: { defaultLocale: 'en', locales: ['en', 'ja'] },
  reactStrictMode: true,
  webpack5: true,
};

module.exports = withSentryConfig(providedExports, {});
