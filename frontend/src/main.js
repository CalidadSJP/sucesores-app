import { createApp } from 'vue'
import App from './App.vue'

// Bootstrap
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';

// FontAwesome
import '@fortawesome/fontawesome-free/css/all.min.css';

// Router
import router from './router';

createApp(App)
  .use(router)
  .mount('#app');
