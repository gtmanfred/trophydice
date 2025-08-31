import { defineConfig } from "vite";

export default defineConfig({
  base: process.env.NODE_ENV === "production" ? "/ui/" : "/",
  root: ".",
  build: {
    outDir: "dist",
  },
  server: {
    proxy: {
      "^/(api|openapi.json|dice)": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
