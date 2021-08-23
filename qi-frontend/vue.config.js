const webpack = require('webpack')

module.exports = {
    pages: {
        index: {
            // pages 的入口
            entry: 'src/main.js',
            // 模板来源
            template: 'public/index.html',
            // 在 dist/index.html 的输出
            filename: 'index.html',
            // 当使用 title 选项时，
            // template 中的 title 标签需要是 <title><%= htmlWebpackPlugin.options.title %></title>
            title: 'Project Qi',
            // 在这个页面中包含的块，默认情况下会包含
            // 提取出来的通用 chunk 和 vendor chunk。
            chunks: ['chunk-vendors', 'chunk-common', 'index']
        },
    },
    devServer: {
        proxy: 'http://localhost:5000'
    },

    productionSourceMap: false,

    css: {
        loaderOptions: {
            css: {},
            less: {
                lessOptions: {
                    modifyVars: {
                        'border-radius-base': '4px',
                    },
                    javascriptEnabled: true,
                },
            }
        },
        extract: false
    },

    configureWebpack: config => {
        config.plugins.push(new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/))
        if (process.env.NODE_ENV === 'production') {
            config.performance = {
                hints: 'warning',
                // 入口起点的最大体积
                maxEntrypointSize: 50000000,
                // 生成文件的最大体积
                maxAssetSize: 30000000,
                // 只给出 js 文件的性能提示
                assetFilter: function (assetFilename) {
                    return assetFilename.endsWith('.js')
                }
            }
        }
    }
}
