<template>
    <div class="menu-container">
      <div class="card mx-auto" style="max-width: 500px;">
        <div class="card-header text-center">
          <h3>Control del Personal</h3>
        </div>
        <div class="card-body d-flex flex-column align-items-center">
          <button @click="goHome" class="home-button">
              <img :src="require('@/assets/home.png')" alt="Home Icon" />
              <span class="card-text">         Inicio</span>
          </button>

          <button @click="$router.push('/form')" class="btn btn-primary mb-3 w-100">
            Formulario Control de Personal
          </button>
          <button @click="showLoginModal = true" class="btn btn-secondary w-100">
            Descargar Registro Control de Personal
          </button>
        </div>
      </div>
  
      <!-- Modal para inicio de sesión -->
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
                  <label for="username" class="form-label">Usuario</label>
                  <input 
                    type="text" 
                    id="username" 
                    v-model="username" 
                    class="form-control" 
                    required 
                    placeholder="Ingresa tu usuario"
                  />
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Contraseña</label>
                  <input 
                    type="password" 
                    id="password" 
                    v-model="password" 
                    class="form-control" 
                    required 
                    placeholder="Ingresa tu contraseña"
                  />
                </div>
                <div class="d-flex justify-content-between">
                  <button type="submit" class="btn btn-success w-45">Iniciar Sesión</button>
                  <button type="button" class="btn btn-secondary w-45" @click="showLoginModal = false">
                    Cancelar
                  </button>
                </div>
              </form>
              <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
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
          this.errorMessage = "Error de autenticación. Intenta nuevamente.";
          console.error("Error en la autenticación:", error);
        }
      },
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
  .menu-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
    background-color: #f8f9fa;
    padding-left: 20px; /* Añadir espacio desde la izquierda */
    padding-right: 20px; /* Añadir espacio desde la derecha */
  }
  
  .card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    background-color: white; /* Fondo blanco de la tarjeta */
    width: 425px;
  }
  
  .card-header {
    background-color: #019c54;
    color: white;
    border-radius: 10px 10px 0 0;
  }
  
  .login-modal {
    position: fixed;
    top: -75px;
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
    background-color: white; /* Fondo blanco del modal */
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

  .home-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-bottom: 20px; /* Espacio entre el botón y el título */
  top: 20px; /* Ajusta según sea necesario */
  left: 20px; /* Ajusta según sea necesario */
  display: flex;
  align-items: center;
}

.home-button img {
  width: 25px;  /* Ajusta el ancho del ícono */
  height: 25px; /* Ajusta la altura del ícono */
  margin-right: 8px;
}

.card-text {
  font-size: 23px; /* Ajusta el tamaño de la palabra según sea necesario */
  color: #000; /* Ajusta el color de la palabra según sea necesario */

}
  </style>
  