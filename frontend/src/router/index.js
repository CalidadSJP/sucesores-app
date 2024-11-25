import { createRouter, createWebHistory } from 'vue-router';
import HomeComponent from '../components/HomeComponent.vue';
import FormComponent from '../components/FormComponent.vue';
import PersonnelComponent from '../components/PersonnelComponent.vue';
import FrecuecyComponent from '../components/FrecuencyComponent.vue';
import WeightComponent from '../components/WeightComponent.vue';
import LoginComponent from '../components/LoginComponent.vue';
import HomeControlComponent from '../components/HomeControlComponent.vue';
import AdditiveStorageForm from '../components/AdditiveStorageForm.vue';

const routes = [
  // Ruta para la página principal
  { path: '/', name: 'Home', component: HomeComponent },

  // Ruta para la página de login
  { path: '/login', name: 'Login', component: LoginComponent },

  // Ruta para el formulario
  { path: '/form', name: 'Form', component: FormComponent },

  // Ruta para la página de personal (protegida)
  { 
    path: '/personnel', 
    name: 'Personnel', 
    component: PersonnelComponent,
    beforeEnter: (to, from, next) => {
      const userId = localStorage.getItem('user_id');
      if (userId) {
        next();  // Si está autenticado, accede
      } else {
        next('/login');  // Si no está autenticado, redirige al login
      }
    }
  },

  // Ruta para la página de frecuencia
  { path: '/frecuency', name: 'Frecuency', component: FrecuecyComponent },

  // Ruta para la página de peso
  { path: '/weight', name: 'WeightComponent', component: WeightComponent },

  
  { path: '/control-home', name: 'HomeControl', component: HomeControlComponent},
  

  { path: '/additive-storage-form', name: 'AdditiveStorageForm', component: AdditiveStorageForm },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
