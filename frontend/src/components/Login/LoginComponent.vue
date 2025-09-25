<template>
  <div class="login-container">
    <h2>Iniciar sesión</h2>
    <button @click="$router.push('/')" class="home-button">
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
  props: ['area'],  // recibimos el área directamente desde la URL
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/login-supervisor`, {
          username: this.username,
          password: this.password,
          area: this.area  // <-- usamos el área que vino desde la URL
        });

        if (response.data.success) {
          localStorage.setItem('user_id', response.data.user_id);
          localStorage.setItem('authToken', response.data.authToken);
          localStorage.setItem('user_area', this.area);

          // Redirigir a la ruta original si existe, o a una por defecto
          const redirectPath = this.$route.query.redirect || this.defaultRedirect(this.area);
          this.$router.push(redirectPath);
        }
        else {
          this.errorMessage = response.data.message || 'Usuario o contraseña incorrectos';
        }
      } catch (error) {
        this.errorMessage = 'Error al iniciar sesión.';
      }
    },
    defaultRedirect(area) {
      if (area === 'Talento Humano') return '/personnel';
      if (area === 'Multas') return '/additive-home';
      if (area === 'Empaque') return '/'
      if (area === 'Laboratorio') return '/additive-register';
      if (area === 'Limpieza') return '/cleaning-home'
      return '/'; // fallback
    }

  }
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