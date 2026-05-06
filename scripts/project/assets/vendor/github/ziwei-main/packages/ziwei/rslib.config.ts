import { defineConfig } from "@rslib/core";

export default defineConfig({
  lib: [
    {
      format: "esm",
      dts: {
        bundle: true,
      },
      output: {
        distPath: {
          root: "./dist/",
        },
      },
      experiments: {
        advancedEsm: true,
      },
    },
    {
      format: "cjs",
      output: {
        distPath: {
          root: "./dist/",
        },
      },
    },
    {
      format: "umd",
      umdName: "ZiWei",
      output: {
        filename: {
          js: "ziweijs.min.js",
        },
        externals: {
          tyme4ts: "tyme4ts",
        },
        distPath: {
          root: "./dist",
        },
      },
    },
  ],
});
