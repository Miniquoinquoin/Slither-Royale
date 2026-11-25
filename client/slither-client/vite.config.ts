import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  base: "/static/",
  build: {
    rollupOptions: {
      input: "src/main.ts",
      output: { entryFileNames: "game.js" },
    },
  },
  server: {
    port: 8081,
    open: true,
  },
});
