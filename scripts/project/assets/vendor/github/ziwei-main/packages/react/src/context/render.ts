import { createContext } from "react";

export interface RenderContextProps {
  showPalaceName: boolean;
  showStem: boolean;
  showBranch: boolean;
  showSelf: boolean;
  showLaiYin: boolean;
  showTransformation: boolean;
}

const defaultRenderContext: RenderContextProps = {
  showPalaceName: true,
  showStem: true,
  showBranch: true,
  showSelf: true,
  showLaiYin: true,
  showTransformation: true,
};

export const RenderContext = createContext<RenderContextProps>(defaultRenderContext);

export function useRender(props?: Partial<RenderContextProps>) {
  return { ...defaultRenderContext, ...props };
}
