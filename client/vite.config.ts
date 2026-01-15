import { resolve } from "path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  resolve: {
    dedupe: [
      "lit",
      "@lit/context",
      "@lit/reactive-element",
      "@lit-labs/signals",
    ],
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        entries: resolve(__dirname, "entries.html"),
      },
    },
  },
  server: {
    port: 5174,
  },
});
