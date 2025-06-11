import { createRouter, createWebHistory } from 'vue-router';
import HomeComponent from '../components/Home/HomeComponent.vue';
import FormComponent from '../components/Personnel/FormComponent.vue';
import PersonnelComponent from '../components/Personnel/PersonnelComponent.vue';
import FrecuecyComponent from '../components/Personnel/FrecuencyComponent.vue';
import WeightComponent from '../components/weight/WeightComponent.vue';
import LoginComponent from '../components/Login/LoginComponent.vue';
import HomeControlComponent from '../components/Home/HomeControlComponent.vue';
import AdditiveStorageForm from '../components/Additive/AdditiveStorageForm.vue';
import AdditiveFiles from '@/components/Additive/AdditiveFiles.vue';
import AdditiveRegister from '@/components/Additive/AdditiveRegister.vue';
import HomeAdditiveComponent from '@/components/Home/HomeAdditiveComponent.vue';
import LoginAdditiveComponent from '@/components/Login/LoginAdditiveComponent.vue';
import AddProductOrProvider from '@/components/Additive/AddProductOrProvider.vue';
import AdditiveRelease from '@/components/Additive/AdditiveRelease.vue';
import AddMaterialOrProvider from '@/components/Packaging/AddMaterialOrProvider.vue';
import MaterialFiles from '@/components/Packaging/MaterialFiles.vue';
import PackagingStorageForm from '@/components/Packaging/PackagingStorageForm.vue';
import MaterialRecord from '@/components/Packaging/MaterialRecord.vue';
import LoginMaterialComponent from '@/components/Login/LoginMaterialComponent.vue';
import LoginAddAdditives from '@/components/Login/LoginAddAdditives.vue';
import LoginAddMaterials from '@/components/Login/LoginAddMaterials.vue';
import InspectionView from '@/components/Personnel/InspectionView.vue';
import LoginInspectionRegister from '@/components/Login/LoginInspectionRegister.vue';
import WeightResume from '@/components/weight/WeightResume.vue';
import WeightRegister from '@/components/weight/WeightRegister.vue';
import ArticlesList from '@/components/Articles/ArticlesList.vue';
import HumidityControl from '@/components/Humidity/HumidityControl.vue';
import ArtFiles from '@/components/Art/ArtFiles.vue';
import ProductMovement from '@/components/Cleaning/ProductMovement.vue';
import ProductManagement from '@/components/Cleaning/ProductManagement.vue';
import PersonnelPenalties from '@/components/Penalties/PersonnelPenalties.vue';
import HomeCleaning from '@/components/Home/HomeCleaning.vue';
import HomePenalties from '@/components/Home/HomePenalties.vue';
import FaultsPenaltiesView from '@/components/Penalties/FaultsPenaltiesView.vue';

const routes = [
  // Ruta para la página principal
  { path: '/', name: 'Home', component: HomeComponent },

  // Ruta para la página de login
  { path: '/login', name: 'Login', component: LoginComponent },

  // Ruta para el formulario
  { path: '/form', name: 'Form', component: FormComponent },

  // Ruta para la página de personal (protegida)
  { path: '/personnel', name: 'Personnel', component: PersonnelComponent,
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

  { path: '/frecuency', name: 'Frecuency', component: FrecuecyComponent },

  { path: '/weight', name: 'WeightComponent', component: WeightComponent },

  { path: '/control-home', name: 'HomeControl', component: HomeControlComponent },

  { path: '/additive-storage-form', name: 'AdditiveStorageForm', component: AdditiveStorageForm },

  { path: '/additive-files', name: 'AdditiveFiles', component: AdditiveFiles },

  { path: '/additive-login', name: 'LoginAdditive', component: LoginAdditiveComponent },

  { path: '/additive-register', component: AdditiveRegister,
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

  { path: '/additive-home', name: 'HomeAdditive', component: HomeAdditiveComponent },

  { path: '/add-product-provider', name: 'AddProductOrProvider', component: AddProductOrProvider,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('authToken');
      const userArea = localStorage.getItem('user_area');

      if (token && userArea === 'Administrativo') {
        next();  // El usuario está autenticado, permite la entrada
      } else {
        next('/add-additives-login');  // Redirige a la página de login si no está autenticado
      }
    },
  },

  { path: '/additive-release', name: 'AdditiveRelease', component: AdditiveRelease },

  { path: '/add-material-provider', name: 'AddMaterialOrProvider', component: AddMaterialOrProvider,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('authToken');
      const userArea = localStorage.getItem('user_area');

      if (token && userArea === 'Administrativo') {
        next();  // El usuario está autenticado, permite la entrada
      } else {
        next('/add-materials-login');  // Redirige a la página de login si no está autenticado
      }
    },
  },

  { path: '/material-files', name: 'MaterialFiles', component: MaterialFiles },

  { path: '/material-login', name: 'LoginMaterialComponent', component: LoginMaterialComponent },

  { path: '/add-additives-login', name: 'LoginAddAdditives', component: LoginAddAdditives },

  { path: '/add-materials-login', name: 'LoginAddMaterials', component: LoginAddMaterials },

  { path: '/material-storage-form', name: 'PackagingStorageForm', component: PackagingStorageForm },

  { path: '/material-register', component: MaterialRecord,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('authToken');
      const userArea = localStorage.getItem('user_area');

      if (token && userArea === 'Empaque') {
        next();  // El usuario está autenticado, permite la entrada
      } else {
        next('/material-login');  // Redirige a la página de login si no está autenticado
      }
    },
  },

  { path: '/inspection-view', name: 'InspectionView', component: InspectionView,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('authToken');
      const userArea = localStorage.getItem('user_area');

      if (token && userArea === 'Calidad') {
        next();  // El usuario está autenticado, permite la entrada
      } else {
        next('/login-inspection-view');  // Redirige a la página de login si no está autenticado
      }
    },
  },

  { path: '/login-inspection-view', name: 'LoginInspectionRegister', component: LoginInspectionRegister },

  { path: '/weight-resume', name: 'WeightResume', component: WeightResume},

  { path: '/weight-register', name: 'WeightRegister', component: WeightRegister},

  { path: '/articles-list', name: 'ArticlesList', component: ArticlesList},

  { path: '/humidity-control', name: 'HumidityControl', component: HumidityControl},

  { path: '/art-files', name: 'ArtFiles', component: ArtFiles},

  { path: '/cleaning-home', name: 'HomeCleaning', component: HomeCleaning},

  { path: '/cleaning-movements', name: 'ProductMovement', component: ProductMovement},

  { path: '/cleaning-products-management', name: 'ProductManagement', component: ProductManagement},

  { path: '/home-penalties', name: 'HomePenalties', component: HomePenalties},

  { path: '/penalties', name: 'PersonnelPenalties', component: PersonnelPenalties},
  
  { path: '/faults-penalties-view', name: 'FaultsPenaltiesView', component: FaultsPenaltiesView}

  

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
