const path = require('path');

module.exports = {
  outputDir: path.resolve(__dirname, 'dist'), // Genera archivos en 'dist'
  indexPath: 'index.html', // Coloca index.html en la raíz de 'dist'
  devServer: {
    proxy: 'http://localhost:5000', // Proxy para el desarrollo local
  },
};
