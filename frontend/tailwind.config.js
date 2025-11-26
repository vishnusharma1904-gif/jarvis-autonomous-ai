/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                jarvis: {
                    primary: '#00f0ff',
                    secondary: '#0099ff',
                    dark: '#0a0e27',
                    darker: '#05070f',
                    accent: '#00ff88',
                    purple: '#b24bf3',
                    pink: '#ff006e',
                },
                neon: {
                    blue: '#00f0ff',
                    purple: '#b24bf3',
                    pink: '#ff006e',
                    green: '#00ff88',
                }
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                mono: ['JetBrains Mono', 'monospace'],
                cyber: ['Orbitron', 'sans-serif'],
            },
            animation: {
                'gradient': 'gradient 3s ease infinite',
                'glow': 'glow 2s ease-in-out infinite',
                'float': 'float 3s ease-in-out infinite',
            },
            keyframes: {
                gradient: {
                    '0%, 100%': { backgroundPosition: '0% 50%' },
                    '50%': { backgroundPosition: '100% 50%' },
                },
                glow: {
                    '0%, 100%': { opacity: '1' },
                    '50%': { opacity: '0.5' },
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0px)' },
                    '50%': { transform: 'translateY(-10px)' },
                },
            },
        },
    },
    plugins: [],
}
