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
  server: {
    port: 5174,
  },
});
