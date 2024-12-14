module.exports = {
    mode: 'jit',
    content: [
        './config/templates/**/*.html',
        './inventory/templates/**/*.html',
        './restaurants/templates/**/*.html',
        './core/templates/**/*.html',
        './config/static/**/*.js',
        './node_modules/flowbite/**/*.js'
    ],
    plugins: [
        require('flowbite/plugin'),
    ],
    theme: {
        extend: {
            colors: {
                'primary': '#020164',
                'secondary': '#FE0C00',
                'ash': 'rgba(30, 30, 30, 1)'
            },
            fontFamily: {
                'poppins': ['Poppins'],
            },
        }
    }
}