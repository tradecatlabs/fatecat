
import styles from '@/styles/Markdown.module.css';
import converter from '@/tools/converter';

// Custom component to render markdown with styles
const StyledMarkdown = ({ content }) => {
    const html = converter.makeHtml(content);
    
    return (
      <div 
        className={styles['markdown-content']}
        dangerouslySetInnerHTML={{ __html: html }}
      />
    );
  };

export default StyledMarkdown;