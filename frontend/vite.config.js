import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  // Load env file from the current directory based on the active mode (development/production)
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [react()],
    server: {
      host: '0.0.0.0',
      port: 5174,
      proxy: {
        '/api': {
          // Fallback to local machine if VITE_API_URL isn't specified in a local .env file
          target: env.VITE_API_URL || 'http://127.0.0.1:8000', 
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    }
  }
})