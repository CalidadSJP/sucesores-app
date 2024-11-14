<template>
  <div class="login-container">
    <h2>Iniciar sesión</h2>
    <button @click="$router.push('/')" class="home-button">
      <img :src="require('@/assets/home.png')" alt="Home Icon" />
    </button>
    <form @submit.prevent="handleLogin"><br>
      <div class="form-group">
        <label for="username">Usuario</label>
        <input 
          type="text" 
          id="username" 
          v-model="username" 
          class="form-control" 
          placeholder="Introduce tu usuario"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Contraseña</label>
        <input 
          type="password" 
          id="password" 
          v-model="password" 
          class="form-control" 
          placeholder="Introduce tu contraseña"
          required
        />
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
      };
    },
    methods: {
      async handleLogin() {
        try {
          const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/login`, {
            username: this.username,
            password: this.password,
          });
  
          if (response.data.success) {
            // Si el login es correcto, guarda el ID del usuario en localStorage
            localStorage.setItem('user_id', response.data.user_id); 
            localStorage.setItem('authToken', response.data.authToken);  // Aquí añadimos el token para autenticación
  
            // Redirige al usuario a la página de gestionar personal
            this.$router.push('/personnel');
          } else {
            // Si el login falla, muestra un mensaje de error
            this.errorMessage = response.data.message || 'Usuario o contraseña incorrectos';
          }
        } catch (error) {
          this.errorMessage = 'Usuario o contraseña incorrectos';
        }
      },
    },
  };
  </script>
  
  <style scoped>

  .login-container {
  max-width: 500px;
  margin: 150px auto; /* Añadido margen superior de 50px */
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  position: relative;
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
  