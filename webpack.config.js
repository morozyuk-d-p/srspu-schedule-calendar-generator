const path = require('path');

const {VueLoaderPlugin} = require('vue-loader');
const Webpack = require('webpack');

module.exports = {
    name: 'main',
    context: __dirname,
    entry: './webpack/js/main.js',
    output: {
        path: path.resolve('./static/webpack/'),
        filename: '[name].js'
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    reactivityTransform: true
                }
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin(),
        new Webpack.DefinePlugin({__VUE_OPTIONS_API__: true, __VUE_PROD_DEVTOOLS__: true})
    ],
    resolve: {
        alias: {
            vue: 'vue/dist/vue.esm-bundler.js'
        },
        extensions: [
            '.vue',
            '.ts',
            '.js'
        ]
    }
}