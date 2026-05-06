import Document, {
  DocumentContext,
  DocumentInitialProps,
  Head,
  Html,
  Main,
  NextScript,
} from 'next/document';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the document language. */
  readonly lang?: string;
}

/** The document root component */
export default class MyDocument extends Document<Props> {
  /**
   * Specify the language on the server-side.
   * @param ctx The context.
   */
  static async getInitialProps(
    ctx: DocumentContext
  ): Promise<DocumentInitialProps & Props> {
    const { lang } = ctx.query;
    return {
      lang: typeof lang === 'string' ? lang : undefined,
      ...(await Document.getInitialProps(ctx)),
    };
  }

  /** Render the virtual DOM structure */
  render(): JSX.Element {
    const { lang } = this.props;
    return (
      <Html
        lang={lang}
        prefix="og: http://ogp.me/ns# article: http://ogp.me/ns/article# website: http://ogp.me/ns/website#"
      >
        <Head />
        <body className="antialiased bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200">
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
