import { pluginReact } from "@rsbuild/plugin-react";
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
    },
    {
      format: "cjs",
      output: {
        distPath: {
          root: "./dist/",
        },
      },
    },
  ],
  output: {
    target: "web",
  },
  plugins: [pluginReact()],
});
