import { defineConfig } from 'vite'

export default defineConfig({
  base: '/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    emptyOutDir: true,
  },
  server: {
    port: 3000,
    proxy: {
      '/auth': 'http://localhost:5000',
      '/user': 'http://localhost:5000',
      '/cziber': 'http://localhost:5000',
      '/company': 'http://localhost:5000',
    }
  }
})
