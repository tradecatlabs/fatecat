export interface Command {
  readonly getDescriptionAsync: (
    ...arg: readonly unknown[]
  ) => string | Promise<string>;
  readonly getObject: (
    ...arg: readonly unknown[]
  ) => unknown | Promise<unknown>;
  readonly alias: string;
  readonly command: string;
  readonly description: string;
}
