import showdown from 'showdown';
// Initialize Showdown converter
const converter = new showdown.Converter({
    tables: true,
    simplifiedAutoLink: true,
    strikethrough: true,
    tasklists: true,
    emoji: true,
  });

export default converter;