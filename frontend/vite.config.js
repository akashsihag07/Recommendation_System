import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// host: true lets the dev server be reached from outside the container if I run
// `npm run dev` instead of the nginx build.
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
  },
});
