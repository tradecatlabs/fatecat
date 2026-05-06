import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    coverage: {
      exclude: ["dist/**"],
    },
    projects: ["packages/*"],
    exclude: ["**/node_modules/**", "**/.git/**", "**/dist/**"],
  },
});
