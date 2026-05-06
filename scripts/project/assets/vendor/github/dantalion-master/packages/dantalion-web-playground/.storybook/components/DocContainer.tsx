import { ReactNode, VFC } from 'react';
import {
  DocsContainer as BaseContainer,
  DocsContainerProps,
  DocsContextProps,
} from '@storybook/addon-docs/blocks';
import merge from 'lodash.merge';
import { useDarkMode } from 'storybook-dark-mode';
import { themes } from '@storybook/theming';

/** Type definition of the required attributes. */
export interface Props extends DocsContainerProps {
  /** The children items. */
  readonly children?: ReactNode;
}

/** The docs container component for Storybook. */
const DocsContainer: VFC<Props> = ({ children, context }) => (
  <BaseContainer
    context={merge<DocsContextProps, DocsContextProps>(context, {
      parameters: {
        docs: { theme: useDarkMode() ? themes.dark : themes.light },
      },
    })}
  >
    {children}
  </BaseContainer>
);
DocsContainer.displayName = 'DocsContainer';

export default DocsContainer;
