module.exports = {
    content: [
        '*.html',
        './node_modules/flowbite/**/*.js'
    ],
    plugins: [
        require('flowbite/plugin'),
    ],
    theme: {
        extend: {
            colors: {
                'primary': 'rgba(14, 34, 84, 1)',
                'secondary': 'rgba(225, 93, 37, 1)',
                'ash': 'rgba(30, 30, 30, 1)'
            }
        }
    }
}