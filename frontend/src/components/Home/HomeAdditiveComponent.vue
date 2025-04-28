<template>
  <header class="menu-header">
    <span class="header-title">Materia Prima / Aditivos / Material de Empaque</span>
  </header>
  <div class="menu-container">
    <div class="nav-buttons">
      <button @click="goHome" class="circle-btn">
        <i class="fas fa-home"></i>
      </button>
      <button v-if="selectedSection" @click="selectedSection = null" class="circle-btn">
        <i class="fas fa-arrow-left"></i>
      </button>
    </div>

    <div v-if="!selectedSection" class="section-grid">
      <div class="card-option" @click="selectedSection = 'additives'">
        <i class="fas fa-flask card-icon"></i>
        <h3>Materia Prima / Aditivos</h3>
        <p>Ingreso, gestión y archivos | Aditivos | Mat. Prima</p>
      </div>
      <div class="card-option" @click="selectedSection = 'packaging'">
        <i class="fas fa-box-open card-icon"></i>
        <h3>Material de Empaque</h3>
        <p>Ingreso, gestión y archivos | Material de Empaque</p>
      </div>
    </div>

    <!-- Sección Aditivos -->
    <div v-if="selectedSection === 'additives'" class="section-grid">
      <div class="card-option" @click="$router.push('/additive-storage-form')">
        <i class="fas fa-file-alt card-icon"></i>
        <h3>Formulario de Ingreso | Aditivos</h3>
        <p>Registrar ingreso de aditivos.</p>
      </div>
      <div class="card-option" @click="$router.push('/additive-files')">
        <i class="fas fa-folder-open card-icon"></i>
        <h3>Archivos | Aditivos</h3>
        <p>Sube o consulta documentación.</p>
      </div>
      <div class="card-option" @click="$router.push('/additive-register')">
        <i class="fas fa-history card-icon"></i>
        <h3>Historial de ingreso | Aditivos</h3>
        <p>Consulta registros anteriores.</p>
      </div>
      <div class="card-option" @click="$router.push('/add-product-provider')">
        <i class="fas fa-truck card-icon"></i>
        <h3>Productos/Proveedores</h3>
        <p>Gestión de productos o proveedores.</p>
      </div>
    </div>

    <!-- Sección Empaque -->
    <div v-if="selectedSection === 'packaging'" class="section-grid">
      <div class="card-option" @click="$router.push('/material-storage-form')">
        <i class="fas fa-file-alt card-icon"></i>
        <h3>Formulario | Material de Empaque</h3>
        <p>Registrar ingreso de material de empaque.</p>
      </div>
      <div class="card-option" @click="$router.push('/material-files')">
        <i class="fas fa-folder-open card-icon"></i>
        <h3>Archivos | Material de Empaque</h3>
        <p>Sube o consulta documentación.</p>
      </div>
      <div class="card-option" @click="$router.push('/add-material-provider')">
        <i class="fas fa-truck card-icon"></i>
        <h3>Productos/Proveedores</h3>
        <p>Gestión de productos o proveedores.</p>
      </div>
      <div class="card-option" @click="$router.push('/material-register')">
        <i class="fas fa-history card-icon"></i>
        <h3>Historial de ingreso | Material de Empaque</h3>
        <p>Consulta registros anteriores.</p>
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
  min-height: 80vh;
  padding: 30px 20px;
  background: #f0f4f8;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header-bar {
  background-color: #019c54;
  color: white;
  width: 100%;
  max-width: 1000px;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 30px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.nav-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 30px;
}

.circle-btn {
  background-color: #019c54;
  border: none;
  border-radius: 50%;
  padding: 14px 18px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  font-size: 20px;
  color: white;
  cursor: pointer;
  transition: transform 0.2s;
}

.circle-btn:hover {
  transform: scale(1.1);
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 30px;
  width: 100%;
  max-width: 1000px;
}

.card-option {
  background: white;
  border-radius: 16px;
  padding: 30px 20px;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.card-option:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.card-option h3 {
  margin-top: 12px;
  margin-bottom: 8px;
  font-size: 1.25rem;
  color: #019c54;
}

.card-option p {
  font-size: 1rem;
  color: #555;
}

.card-icon {
  font-size: 2.5rem;
  color: #019c54;
}


.menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #019c54;
  color: white;
  padding: 20px 40px;
}

.header-title {
  font-size: 1.8rem;
  font-weight: bold;
}
</style>
