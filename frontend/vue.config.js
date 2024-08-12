const path = require("path");
const { VuetifyPlugin } = require("webpack-plugin-vuetify");

module.exports = {
  outputDir: path.resolve(__dirname, "../formula_1/static/app"),
  publicPath: "/",
  devServer: {
    devMiddleware: {
      writeToDisk: (filePath) => {
        return !/hot-update/i.test(filePath); // you can change it to whatever you need
      },
    },
  },
  // disable hashes in filenames
  filenameHashing: false,
  // delete HTML related webpack plugins
  chainWebpack: (config) => {
    config.plugins.delete("html");
    config.plugins.delete("preload");
    config.plugins.delete("prefetch");
  },
  configureWebpack: {
    plugins: [new VuetifyPlugin({ autoImport: true })],
  },
};
