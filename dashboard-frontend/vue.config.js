const path = require('path')
const { mergeSassVariables } = require('@vuetify/cli-plugin-utils')
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  outputDir: './dist/',
  assetsDir: 'static/frontend',
  transpileDependencies: ['vuetify'],
  configureWebpack: {
    resolve: {
      alias: {
        '@themeConfig': path.resolve(__dirname, 'themeConfig.js'),
        '@core': path.resolve(__dirname, 'src/@core'),
        '@axios': path.resolve(__dirname, 'src/plugins/axios.js'),
        '@user-variables': path.resolve(__dirname, 'src/styles/variables.scss'),
      },
    },
  },
  chainWebpack: config => {
    const modules = ['vue-modules', 'vue', 'normal-modules', 'normal']
    config.plugin('BundleTracker').use(BundleTracker, [{filename: './webpack-stats.json'}])

    modules.forEach(match => {
      config.module
        .rule('sass')
        .oneOf(match)
        .use('sass-loader')
        .tap(opt => mergeSassVariables(opt, "'@/styles/variables.scss'"))
      config.module
        .rule('scss')
        .oneOf(match)
        .use('sass-loader')
        .tap(opt => mergeSassVariables(opt, "'@/styles/variables.scss';"))
    })
  },
}