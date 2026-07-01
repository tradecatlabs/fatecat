import { useEffect, useState } from 'react';

export function useViewportWidth(defaultWidth: number): number {
  const [width, setWidth] = useState(() =>
    typeof window === 'undefined' ? defaultWidth : window.innerWidth,
  );

  useEffect(() => {
    if (typeof window === 'undefined') {
      return undefined;
    }

    function handleResize() {
      setWidth(window.innerWidth);
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return width;
}
