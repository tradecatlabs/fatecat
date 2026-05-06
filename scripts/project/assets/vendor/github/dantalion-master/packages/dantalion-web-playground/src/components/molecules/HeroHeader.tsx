import type { VFC } from 'react';
import Logo from '../atoms/Logo';

export interface Props {
  readonly __?: unknown;
}

const HeroHeader: VFC<Props> = () => (
  <header className="bg-gray-200 flex">
    <h1>
      <Logo />
    </h1>
  </header>
);
HeroHeader.displayName = 'HeroHeader';

export default HeroHeader;
