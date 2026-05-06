module.exports = {
  addons: [
    '@storybook/addon-essentials',
    {
      name: '@storybook/addon-postcss',
      options: { postcssLoaderOptions: { implementation: require('postcss') } },
    },
    'storybook-dark-mode',
  ],
  core: { builder: 'webpack5' },
  stories: ['../src/**/*.stories.mdx', '../src/**/*.stories.@(js|jsx|ts|tsx)'],
  typescript: { check: true, reactDocgen: 'react-docgen-typescript' },
};
