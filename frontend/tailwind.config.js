/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        swift: {
          bg: '#060B18',
          surface: '#0D1626',
          card: '#111C2E',
          border: '#1E2D47',
          accent: '#00D4FF',
          accentDim: '#0099BB',
          green: '#00FF88',
          orange: '#FF7A00',
          red: '#FF3B3B',
          purple: '#8B5CF6',
          text: '#E2E8F0',
          muted: '#64748B',
        }
      },
      fontFamily: {
        display: ['Rajdhani', 'sans-serif'],
        body: ['DM Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'slide-in': 'slideIn 0.3s ease-out',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        glow: {
          from: { boxShadow: '0 0 10px #00D4FF33' },
          to: { boxShadow: '0 0 25px #00D4FF88, 0 0 50px #00D4FF33' },
        },
        slideIn: {
          from: { opacity: 0, transform: 'translateX(-10px)' },
          to: { opacity: 1, transform: 'translateX(0)' },
        }
      }
    }
  },
  plugins: []
}