import { createRouter, createWebHistory } from 'vue-router';
import HomeComponent from '../components/Home/HomeComponent.vue';
import FormComponent from '../components/Personnel/FormComponent.vue';
import PersonnelComponent from '../components/Personnel/PersonnelComponent.vue';
import FrecuecyComponent from '../components/Personnel/FrecuencyComponent.vue';
import WeightComponent from '../components/WeightComponent.vue';
import LoginComponent from '../components/Login/LoginComponent.vue';
import HomeControlComponent from '../components/Home/HomeControlComponent.vue';
import AdditiveStorageForm from '../components/Additive/AdditiveStorageForm.vue';
import AdditiveFiles from '@/components/Additive/AdditiveFiles.vue';
import AdditiveRegister from '@/components/Additive/AdditiveRegister.vue';
import HomeAdditiveComponent from '@/components/Home/HomeAdditiveComponent.vue';
import LoginAdditiveComponent from '@/components/Login/LoginAdditiveComponent.vue';
import AddProductOrProvider from '@/components/Additive/AddProductOrProvider.vue';
import AdditiveRelease from '@/components/Additive/AdditiveRelease.vue';

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
      const token = localStorage.getItem('authToken');
      const userArea = localStorage.getItem('user_area');
    
    if (token && userArea === 'Talento Humano') {
        next();  // Si está autenticado, accede
      } else {
        next('/login');  // Si no está autenticado, redirige al login
      }
    }
  },

  // Ruta para la página de frecuencia
  { path: '/frecuency', name: 'Frecuency', component: FrecuecyComponent },

  { path: '/weight', name: 'WeightComponent', component: WeightComponent },

  { path: '/control-home', name: 'HomeControl', component: HomeControlComponent},
  
  { path: '/additive-storage-form', name: 'AdditiveStorageForm', component: AdditiveStorageForm },

  { path: '/additive-files', name: 'AdditiveFiles', component: AdditiveFiles},

  {path: '/additive-login', name: 'LoginAdditive', component: LoginAdditiveComponent},

  {
    path: '/additive-register',
    component: AdditiveRegister,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('authToken');
      const userArea = localStorage.getItem('user_area');
    
    if (token && userArea === 'Laboratorio') {
        next();  // El usuario está autenticado, permite la entrada
      } else {
        next('/additive-login');  // Redirige a la página de login si no está autenticado
      }
    },
  },

  {path: '/additive-home', name: 'HomeAdditive', component: HomeAdditiveComponent},

  {path: '/add-product-provider', name: 'AddProductOrProvider', component: AddProductOrProvider},

  {path: '/additive-release', name: 'AdditiveRelease', component: AdditiveRelease}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
