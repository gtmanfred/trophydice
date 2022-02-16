import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: process.env.NODE_ENV === 'production' ? '/ui/' : '/',
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    proxy: {
      "^/(api|openapi.json|dice)": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/socket.io": {
        target: "ws://localhost:8000",
        ws: true,
      },
    },
  },
});
