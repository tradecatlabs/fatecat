import '../src/styles/global.css';
import DocsContainer from './components/DocContainer';

export const parameters = {
  actions: { argTypesRegex: '^on[A-Z].*' },
  controls: { matchers: { color: /(background|color)$/i, date: /Date$/ } },
  darkMode: { darkClass: 'dark', stylePreview: true },
  docs: { container: DocsContainer },
  viewMode: 'docs',
};
