import { createContext, type PropsWithChildren, use } from "react";

export function createContainer<T>(useCustomHookFn: () => T) {
  const ContainerContext = createContext<T | null>(null);
  const Provider = ({ children }: PropsWithChildren) => {
    const result = useCustomHookFn();

    return <ContainerContext value={result}>{children}</ContainerContext>;
  };

  const useContainer = () => {
    return use(ContainerContext) as T;
  };

  return { Provider, useContainer };
}
