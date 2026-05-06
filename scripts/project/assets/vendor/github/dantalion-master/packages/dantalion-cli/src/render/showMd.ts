import marked from 'marked';
import TerminalRenderer from 'marked-terminal';

marked.setOptions({ renderer: new TerminalRenderer() });

/**
 * Render the markdown document for terminal.
 * @param result The markdown document.
 */
// eslint-disable-next-line no-console
export default (source: string): void => console.info(marked(source));
