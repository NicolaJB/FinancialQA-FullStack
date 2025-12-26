/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./app/**/*.{js,ts,jsx,tsx}",  // If using the `app/` directory in Next.js
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Geist', 'Arial', 'Helvetica', 'sans-serif'],
        mono: ['Geist Mono', 'Courier', 'monospace'],
      },
    },
  },
  plugins: [],
};
