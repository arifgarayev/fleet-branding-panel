/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}",
            "./dist/**/*.{html,js}",
            "../templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require('@tailwindcss/forms'),
    require('@tailwindcss/typography')],
}
