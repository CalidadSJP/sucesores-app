<template>
  <div class="menu-container">
    <div class="card mx-auto" style="max-width: 900px;">
      <div class="card-header text-center">
        <h3>Ingreso Materia Prima/Material de Empaque/Aditivos</h3>
      </div>
      <div class="card-body">
        <!-- Botón de Inicio único -->
        <div class="d-flex justify-content-center mb-4">
          <button @click="goHome" class="home-button">
            <img :src="require('@/assets/home.png')" alt="Home Icon" />
            <span class="card-text">Inicio</span>
          </button>
        </div>

        <div class="d-flex">
          <!-- Sección Materia Prima/Aditivo -->
          <div class="section-left w-50 pe-3">
            <h4 class="text-center mb-3">Materia Prima/Aditivos</h4><br>
            <button @click="$router.push('/additive-storage-form')" class="btn btn-success mb-3 w-100">
              Formulario-Ingreso de Aditivos
            </button>
            <button @click="$router.push('/additive-register')" class="btn btn-success mb-3 w-100">
              Consulta Historial-Ingreso de Aditivos
            </button>
            <button @click="$router.push('/additive-files')" class="btn btn-secondary mb-3 w-100">
              Ingresar Archivos-Aditivos
            </button>
            <button @click="$router.push('/add-product-provider')" class="btn btn-secondary mb-3 w-100">
              Agregar Producto o Proveedor
            </button>
          </div>

          <!-- Sección Material de Empaque -->
          <div class="section-right w-50 ps-3">
            <h4 class="text-center mb-3">Material de Empaque</h4><br>
            <button @click="$router.push('/material-storage-form')" class="btn btn-success mb-3 w-100">
              Formulario-Ingreso de Material de Empaque
            </button>
            <button @click="$router.push('/material-register')" class="btn btn-success mb-3 w-100">
              Consulta Historial-Material de Empaque
            </button>
            <button @click="$router.push('/material-files')" class="btn btn-secondary mb-3 w-100">
              Ingresar Archivos-Material de Empaque
            </button>
            <button @click="$router.push('/add-material-provider')" class="btn btn-secondary mb-3 w-100">
              Agregar Producto o Proveedor
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
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
  height: 90vh;
  background-color: #ffffff;
  padding: 20px;
}

.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  background-color: #f9f9f9;
  width: 100%;
}

.card-header {
  background-color: #019c54;
  color: white;
  border-radius: 10px 10px 0 0;
}

.section-left,
.section-right {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.home-button {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.home-button img {
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
