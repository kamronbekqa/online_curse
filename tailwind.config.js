/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        'brand': '#4f46e5',
        'brand-hover': '#4338ca',
        'dark': '#111827',
      }
    },
  },
  plugins: [],
}
