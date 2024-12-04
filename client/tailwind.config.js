const flowbite = require("flowbite-react/tailwind");

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}", flowbite.content()],
  theme: {
    extend: {
      colors: {
        primary: "#020164",
        secondary: "#FE0C00",
        ash: "rgba(30, 30, 30, 1)",
      },
      fontFamily: {
        poppins: ["Poppins"],
      },
    },
  },
  plugins: [flowbite.plugin()],
};
