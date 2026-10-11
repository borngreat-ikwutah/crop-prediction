import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { TanStackRouterVite } from '@tanstack/router-plugin/vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    TanStackRouterVite({
      routesDirectory: './src/routes',
      generatedRouteTree: './src/routeTree.gen.ts',
      quoteStyle: 'single',
    }),
    react(),
  ],
  server: {
    host: '0.0.0.0', // Listen on all network interfaces for phone access
    port: 3000,
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
  },
});
