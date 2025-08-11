import path from "path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    }
  },
  // add for other routs to allow to loads the site
  preview: {
    allowedHosts: ['webscraper-forntend.onrender.com'],
    host: '0.0.0.0',
    port: process.env.PORT || 4173
  },
})