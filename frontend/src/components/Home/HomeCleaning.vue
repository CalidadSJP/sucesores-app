<template>
  <div class="menu-personal">
    <header class="menu-header">
      <span class="header-title">Limpieza</span>
    </header>

    <div class="nav-buttons-centered">
      <button @click="goHome" class="circle-btn">
        <i class="fas fa-home"></i>
      </button>
      <button v-if="selectedSection" @click="selectedSection = null" class="circle-btn">
        <i class="fas fa-arrow-left"></i>
      </button>
    </div>


    <main class="content-wrapper">

      <section class="menu-options">
        <div class="card-option" @click="$router.push('/cleaning-movements')">
          <i class="fas fa-hand-sparkles card-icon"></i>
          <h3>Kardex de Limpieza</h3>
          <p>Registrar el ingreso y egreso de los implementos y productos de limpieza.</p>
        </div>
        <div class="card-option" @click="$router.push('/cleaning-products-management')">
          <i class="fas fa-lines-leaning card-icon"></i>
          <h3>Listado | Limpieza</h3>
          <p>Visualiza y edita el listado de productos e implementos de limpieza.</p>
        </div>
        <div class="card-option" @click="$router.push('/cleaning-product-record')">
          <i class="fas fa-list-check card-icon"></i>
          <h3>Visualización - Registros | Kardex de Limpieza</h3>
          <p>Visualiza los cambios en el inventario de limpieza.</p>
        </div>
        <div class="card-option" @click="downloadExcel">
          <i class="fas fa-download card-icon"></i>
          <h3>Descargar Registro</h3>
          <p>Descarga los movimientos del inventario de limpieza.</p>
        </div>

      </section>

    </main>
  </div>
</template>



<script>

export default {
  data() {
    return {

    };
  },
  methods: {
    goHome() {
      this.$router.push('/');
    },

    downloadExcel() {
      const url = `${process.env.VUE_APP_API_URL}/api/download-cleaning-movements`;
      window.open(url, '_blank');
    },
  },
};
</script>

<style scoped>
.menu-personal {
  min-height: 100vh;
  background: linear-gradient(to bottom right, #e5f5ee, #ffffff);
  display: flex;
  flex-direction: column;
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

.back-button {
  background: white;
  border: none;
  color: #019c54;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.back-button:hover {
  background: #e0e0e0;
}

.content-wrapper {
  padding: 40px 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.intro-text {
  text-align: center;
  max-width: 700px;
  margin-bottom: 40px;
}

.intro-text h2 {
  font-size: 2rem;
  color: #019c54;
  margin-bottom: 10px;
}

.intro-text p {
  font-size: 1.1rem;
  color: #333;
}

.menu-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px;
  font-size: 1.1rem;
  font-weight: bold;
  border: none;
  border-radius: 12px;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.menu-button i {
  font-size: 1.5rem;
}


.text-danger {
  color: #dc3545;
}

.w-45 {
  width: 45%;
}

.menu-options {
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

.nav-buttons {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 10px;
}


.nav-buttons-centered {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin: 20px 0 10px;
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
</style>
