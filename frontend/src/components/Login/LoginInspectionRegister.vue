<template>
    <div class="login-container">
      <h2>Iniciar sesión</h2>
      <button @click="$router.push('/control-home')" class="home-button">
        <img :src="require('@/assets/home.png')" alt="Home Icon" />
      </button>
      <form @submit.prevent="handleLogin"><br>
        <div class="form-group">
          <label for="username">Usuario</label>
          <input type="text" id="username" v-model="username" class="form-control" placeholder="Introduce tu usuario"
            required />
        </div>
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input type="password" id="password" v-model="password" class="form-control"
            placeholder="Introduce tu contraseña" required />
        </div>
        <button type="submit" class="btn btn-success">Iniciar sesión</button>
      </form>
      <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        errorMessage: '', // Para mostrar mensajes de error
        area: 'Calidad',
      };
    },
    methods: {
      async handleLogin() {
        try {
          // Envía la solicitud con el área ya seteada
          const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/login-supervisor`, {
            username: this.username,
            password: this.password,
            area: this.area,  // No es necesario que el usuario la elija, ya está definida
          });
  
          // Verifica si la respuesta fue exitosa
          if (response.data.success) {
            // Si el login es correcto, guarda el ID del usuario, el token y el área en localStorage
            localStorage.setItem('user_id', response.data.user_id);
            localStorage.setItem('authToken', response.data.authToken);  // Aquí añadimos el token para autenticación
            localStorage.setItem('user_area', "Calidad");  // Guardamos el área del usuario
  
            // Redirige a la página de registro de aditivos
            this.$router.push('/inspection-view');
          } else {
            // Si el login falla, muestra un mensaje de error
            this.errorMessage = response.data.message || 'Usuario o contraseña incorrectos';
          }
        } catch (error) {
          // En caso de error, muestra un mensaje genérico
          this.errorMessage = 'Usuario o contraseña incorrectos';
        }
      }
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    max-width: 500px;
    margin: 150px auto;
    /* Centra el contenedor con margen superior adecuado */
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
    position: relative;
    width: 100%;
    /* Asegura que ocupe el 100% del ancho disponible */
    box-sizing: border-box;
    /* Incluye el padding dentro del ancho total */
  }
  
  /* Ajustes para pantallas pequeñas */
  @media (max-width: 600px) {
    .login-container {
      margin: 50px auto;
      /* Menor margen superior en pantallas pequeñas */
      padding: 20px;
      /* Asegura que haya espacio en todos los lados */
      width: 90%;
      /* El contenedor ocupa el 90% del ancho disponible en dispositivos pequeños */
    }
  }
  
  .home-button {
    position: absolute;
    top: 20px;
    right: 20px;
    background: none;
    border: none;
    cursor: pointer;
  }
  
  .home-button img {
    width: 24px;
    height: 24px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-control {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
  }
  
  .btn {
    width: 100%;
    padding: 10px;
    font-size: 16px;
  }
  </style>