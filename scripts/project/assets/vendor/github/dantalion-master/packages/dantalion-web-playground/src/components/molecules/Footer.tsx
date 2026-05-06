import { Children, ReactNode, ReactNodeArray, VFC } from 'react';
import Logo from '../atoms/Logo';
import FooterNavigation from './FooterNavigation';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the author name. */
  readonly author?: ReactNode;
  /** The children items. */
  readonly children?: ReactNodeArray;
}

/** The footer component */
const Footer: VFC<Props> = ({ author, children }) => (
  <footer
    className="nm-flat-gray-300-xs mt-4 py-4 text-gray-700 text-sm dark:nm-flat-gray-600-xs dark:text-gray-200"
    role="contentinfo"
  >
    <nav className="flex flex-col mx-auto sm:flex-row lg:container">
      <div className="hidden flex-shrink xl:block">
        <Logo />
      </div>
      <div className="flex flex-grow items-center justify-center">
        <FooterNavigation author={author} />
      </div>
      <div className="flex flex-col flex-shrink p-4 lg:flex-row">
        {Children.toArray(children).map((child, index) => (
          // eslint-disable-next-line react/no-array-index-key
          <div className="flex-shrink p-4" key={index}>
            {child}
          </div>
        ))}
      </div>
    </nav>
  </footer>
);
Footer.displayName = 'Footer';

export default Footer;
