import { useCallback } from 'react';

/**
 * The type definition that gets the whether the current environment
 * is server-side.
 */
export type IsSsr = (invert?: boolean) => boolean;

/** Get the whether the current environment is server-side. */
const useIsSsr = (): IsSsr =>
  useCallback<IsSsr>(
    (n) => (n ? typeof window !== 'undefined' : typeof window === 'undefined'),
    []
  );

export default useIsSsr;
