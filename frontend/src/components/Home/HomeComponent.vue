<template>
  <div class="home-wrapper">
    <header class="hero">
      <img src="@/assets/logo-sucesores-app.png" alt="Logo" class="logo" />
      <h1>Bienvenido a Sucesores App - Calidad</h1>
    </header>

    <section class="menu-section">
      <div class="menu-grid">
        <div class="menu-card">
          <i class="fas fa-users icon"></i>
          <h3>Personal</h3>
          <router-link to="/control-home" class="btn">➤</router-link>
        </div>
        <div class="menu-card">
          <i class="fas fa-boxes icon"></i>
          <h3>Material Empaque/Aditivos</h3>
          <router-link to="/additive-home" class="btn">➤</router-link>
        </div>
        <div class="menu-card">
          <i class="fas fa-balance-scale icon"></i>
          <h3>Control de Pesos</h3>
          <router-link to="/weight" class="btn">➤</router-link>
        </div>
        <div class="menu-card">
          <i class="fas fa-tint icon"></i>
          <h3>Control de Humedades</h3>
          <router-link to="/humidity-control" class="btn">➤</router-link>
        </div>
        <div class="menu-card">
          <i class="fas fa-triangle-exclamation icon"></i>
          <h3>Faltas y Multas</h3>
          <router-link to="/home-penalties" class="btn">➤</router-link>
        </div>
        <div class="menu-card">
          <i class="fas fa-broom icon"></i>
          <h3>Limpieza</h3>
          <router-link to="/cleaning-home" class="btn">➤</router-link>
        </div>
      </div>
    </section>

    <footer class="footer">
      © 2024 Sucesores de Jacobo Paredes S.A
      <br><br>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomeComponent',
};
</script>

<style scoped>
.home-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.hero {
  text-align: center;
  padding: 0.25rem 0.1rem;
  background-image: url('https://wallpapers.com/images/hd/plain-dark-green-wallpaper-krt3ve53xrh5dy16.jpg');
  /* Cambia la ruta si usas una URL externa */
  background-size: cover;
  background-position: center;
  color: white;
  position: relative;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.hero::before {
  content: '';
  position: absolute;
  inset: 0;
}

.hero>* {
  position: relative;
  z-index: 1;
}

.logo {
  width: 120px;
  margin-bottom: 1rem;
}

.hero h1 {
  font-size: 2.1rem;
  margin-bottom: 0.5rem;
}

.hero p {
  font-size: 1.2rem;
}

.menu-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem 1rem;
  background: linear-gradient(to right, #e8f5e9, #f1f8e9);
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 2rem;
  width: 100%;
  max-width: 1000px;
}

.menu-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.menu-card:hover {
  transform: translateY(-5px);
}

.icon {
  font-size: 2.5rem;
  color: #019c54;
  margin-bottom: 1rem;
}

.btn {
  margin-top: 1rem;
  display: inline-block;
  padding: 0.5rem 1.2rem;
  border-radius: 20px;
  background-color: #019c54;
  color: white;
  text-decoration: none;
  transition: background 0.3s;
}

.btn:hover {
  background-color: #01693a;
}

.footer {
  text-align: center;
  padding: 1rem;
  background: linear-gradient(to right, #e8f5e9, #f1f8e9);
  color: #555;
}
</style>
