// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeComponent from '../components/HomeComponent.vue';  
import FormComponent from '../components/FormComponent.vue';
import PersonnelComponent from '../components/PersonnelComponent.vue';
import FrecuecyComponent from '../components/FrecuencyComponent.vue';
import WeightComponent from '../components/WeightComponent.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeComponent
  },
  {
    path: '/form',
    name: 'Form',
    component: FormComponent
  },
  {
    path: '/personnel',
    name: 'Personnel',
    component: PersonnelComponent
  },
  {
    path: '/frecuency',
    name: 'Frecuency',
    component: FrecuecyComponent
  },
  {
    path: '/weight',
    name: 'WeightComponent',
    component: WeightComponent
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
