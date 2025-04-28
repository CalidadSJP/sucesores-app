<template>
  <div class="menu-personal">
    <header class="menu-header">
      <span class="header-title">Personal</span>
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
        <div class="card-option" @click="$router.push('/form')">
          <i class="fas fa-clipboard-check card-icon"></i>
          <h3>Formulario de Control de Prácticas del Personal</h3>
          <p>Registrar prácticas del personal de planta.</p>
        </div>
        <div class="card-option" @click="$router.push('/inspection-view')">
          <i class="fas fa-eye card-icon"></i>
          <h3>Registro de Prácticas del Personal</h3>
          <p>Visualiza y consulta los registros anteriores.</p>
        </div>
        <div class="card-option" @click="showLoginModal = true">
          <i class="fas fa-download card-icon"></i>
          <h3>Descargar Registro</h3>
          <p>Exporta la información en formato Excel.</p>
        </div>
        <div class="card-option" @click="$router.push('/personnel')">
          <i class="fas fa-users-cog card-icon"></i>
          <h3>Gestión de Personal</h3>
          <p>Administra los datos del personal de planta.</p>
        </div>
      </section>

    </main>

    <!-- Modal -->
    <div v-if="showLoginModal" class="login-modal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Descarga del Registro</h5>
            <button type="button" class="btn-close" @click="showLoginModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="authenticate">
              <div class="mb-3">
                <label for="username">Usuario</label>
                <input type="text" id="username" v-model="username" class="form-control" required>
              </div>
              <div class="mb-3">
                <label for="password">Contraseña</label>
                <input type="password" id="password" v-model="password" class="form-control" required>
              </div>
              <div class="d-flex justify-content-between">
                <button type="submit" class="btn btn-success w-45">Iniciar Sesión</button>
                <button type="button" class="btn btn-secondary w-45" @click="showLoginModal = false">Cancelar</button>
              </div>
              <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import axios from "axios";

export default {
  data() {
    return {
      showLoginModal: false,
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    goHome() {
      this.$router.push('/');
    },
    async authenticate() {
      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/api/login-supervisor`,
          {
            username: this.username,
            password: this.password,
            area: "Calidad", // Área fija asignada a esta página
          }
        );

        if (response.data.success) {
          this.errorMessage = "";
          this.showLoginModal = false; // Cierra el modal
          this.downloadExcel(); // Descarga el Excel
        } else {
          this.errorMessage = response.data.message || "Usuario o contraseña incorrectos.";
        }
      } catch (error) {
        this.errorMessage = "Usuario o contraseña incorrectos.";
        console.error("Error en la autenticación:", error);
      }
    }
    ,
    async downloadExcel() {
      try {
        const response = await axios.get(
          `${process.env.VUE_APP_API_URL}/api/download-inspection`,
          { responseType: "blob" }
        );
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "registro-control-personal.xlsx");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error("Error al descargar el archivo Excel:", error);
        alert("Error al descargar el archivo Excel.");
      }
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

/* Modal y helpers */
.login-modal {
  position: fixed;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-dialog {
  width: 325px;
}

.modal-content {
  border-radius: 10px;
  overflow: hidden;
  background-color: white;
}

.modal-header {
  background-color: #019c54;
  color: white;
  padding: 15px;
}

.modal-header .btn-close {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
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
