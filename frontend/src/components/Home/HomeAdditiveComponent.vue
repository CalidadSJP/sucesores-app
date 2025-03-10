<template>
  <div class="menu-container">
    <div class="card mx-auto" style="max-width: 900px;">
      <div class="card-header text-center">
        <h3>Ingreso Materia Prima/Material de Empaque/Aditivos</h3>
      </div>
      <div class="card-body">
        <!-- Botones de Inicio y Volver -->
        <div class="d-flex justify-content-center mb-4">
          <button @click="goHome" class="nav-button me-3">
            <img :src="require('@/assets/home.png')" alt="Home Icon" />
            <span class="card-text">Inicio</span>
          </button>
          <button v-if="selectedSection" @click="selectedSection = null" class="nav-button">
            <img :src="require('@/assets/back-arrow.png')" alt="Back Icon" />
            <span class="card-text">Volver</span>
          </button>
        </div>

        <!-- Botones principales -->
        <div v-if="!selectedSection" class="d-flex justify-content-center">
          <button @click="selectedSection = 'additives'" class="btn btn-success me-3">
            Materia Prima / Aditivos
          </button>
          <button @click="selectedSection = 'packaging'" class="btn btn-success">
            Material de Empaque
          </button>
        </div>

        <!-- Sección Materia Prima/Aditivos -->
        <div v-if="selectedSection === 'additives'" class="w-100">
          <h4 class="text-center mb-3">Materia Prima/Aditivos</h4><br>
          <button @click="$router.push('/additive-storage-form')" class="btn btn-success mb-3 w-100">
            Formulario | Ingreso de Aditivos
          </button>
          <button @click="$router.push('/additive-files')" class="btn btn-success mb-3 w-100">
            Ingresar Archivos | Aditivos
          </button>
          <button @click="$router.push('/additive-register')" class="btn btn-secondary mb-3 w-100">
            Consulta Historial | Ingreso de Aditivos
          </button>
          <button @click="$router.push('/add-product-provider')" class="btn btn-secondary mb-3 w-100">
            Listar | Agregar | Productos o Proveedores
          </button>
        </div>

        <!-- Sección Material de Empaque -->
        <div v-if="selectedSection === 'packaging'" class="w-100">
          <h4 class="text-center mb-3">Material de Empaque</h4><br>
          <button @click="$router.push('/material-storage-form')" class="btn btn-success mb-3 w-100">
            Formulario | Ingreso de Material de Empaque
          </button>
          <button @click="$router.push('/material-files')" class="btn btn-success mb-3 w-100">
            Ingresar Archivos | Material de Empaque
          </button>
          <button @click="$router.push('/add-material-provider')" class="btn btn-secondary mb-3 w-100">
            Listar | Agregar | Productos o Proveedores
          </button>
          <button @click="$router.push('/material-register')" class="btn btn-secondary mb-3 w-100">
            Consulta Historial | Material de Empaque
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedSection: null, // Al inicio, no se muestra ninguna sección
    };
  },
  methods: {
    goHome() {
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>
.menu-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 85vh;
  background-color: #ffffff;
  padding: 20px;
}

.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  background-color: #f9f9f9;
  width: 500px;
}

.card-header {
  background-color: #019c54;
  color: white;
  border-radius: 10px 10px 0 0;
}

.nav-button {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.nav-button img {
  width: 25px;
  height: 25px;
  margin-right: 8px;
}

.card-text {
  font-size: 23px;
  color: #000;
}

h4 {
  color: #019c54;
}
</style>
