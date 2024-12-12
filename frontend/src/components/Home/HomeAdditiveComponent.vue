<template>
    <div class="menu-container">
      <div class="card mx-auto" style="max-width: 500px;">
        <div class="card-header text-center">
          <h3>Ingreso Materia Prima/Material de Empaque/Aditivos</h3>
        </div>
        <div class="card-body d-flex flex-column align-items-center">
          <button @click="goHome" class="home-button">
              <img :src="require('@/assets/home.png')" alt="Home Icon" />
              <span class="card-text">         Inicio</span>
          </button>

          <button @click="$router.push('/additive-storage-form')" class="btn btn-primary mb-3 w-100">
            Formulario-Ingreso de Aditivos
          </button>
          <button @click="$router.push('/additive-register')" class="btn btn-secondary mb-3 w-100">
            Consulta historial-Ingreso de Aditivos
          </button>
          <button @click="$router.push('/additive-files')" class="btn btn-primary mb-3 w-100">
            Ingresar archivos-Aditivos
          </button>
        </div>
      </div>
  
    </div>
  </template>
  
  <script>
  
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
    },
  };
  </script>
  
  <style scoped>
  .menu-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
    background-color: #ffffff;
    border: 1px solid #ccc;
    padding-left: 20px; /* Añadir espacio desde la izquierda */
    padding-right: 20px; /* Añadir espacio desde la derecha */
  }
  
  .card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    background-color: #f9f9f9; /* Fondo blanco de la tarjeta */
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
  