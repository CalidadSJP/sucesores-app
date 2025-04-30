import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import router from './router'; 
import '@fortawesome/fontawesome-free/css/all.min.css';


createApp(App)
  .use(router)
  .mount('#app');
