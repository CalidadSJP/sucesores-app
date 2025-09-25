<template>
  <div class="home-wrapper d-flex flex-wrap">
    <header class="hero menu-header">
      <img src="@/assets/logo-sucesores-app.png" alt="Logo" class="logo" />
      <h1>Bienvenido a Sucesores App - Calidad</h1>
    </header>

    <section class="menu-section">
      <div class="menu-grid">
        <div class="menu-card" v-for="option in menuOptions" :key="option.label">
          <div class="d-flex align-items-center icon-container">
            <i :class="option.icon" class="icon"></i>
            <h2>{{ option.label }}</h2>
          </div>
          <router-link :to="option.link" class="btn">➤</router-link>
        </div>
        <div class="footer-text">
          © 2024 Sucesores de Jacobo Paredes S.A
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      menuOptions: [
        { label: 'Personal', icon: 'fas fa-users', link: '/control-home' },
        { label: 'Material de Empaque y Aditivos', icon: 'fas fa-boxes', link: '/additive-home' },
        { label: 'Control de Pesos', icon: 'fas fa-balance-scale', link: '/weight' },
        { label: 'Control de Humedades', icon: 'fas fa-tint', link: '/humidity-control' },
        { label: 'Faltas y Multas', icon: 'fas fa-triangle-exclamation', link: '/home-penalties' },
        { label: 'Limpieza', icon: 'fas fa-broom', link: '/cleaning-home' },
        { label: 'Control de Sondas', icon: 'fas fa-industry', link: '/pieces-inspection' },
      ]
    };
  }
};
</script>

<style scoped>
@keyframes fadeSlideUp {
  0% { opacity: 0; transform: translateY(30px); }
  100% { opacity: 1; transform: translateY(0); }
}

@keyframes bounceIcon {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.home-wrapper {
  display: flex;
  flex-wrap: wrap;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f4fdf6;
}

.menu-header {
  background-color: #019c54;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  width: 50%;
  text-align: center;
  color: white;
}

.logo {
  width: 150px;
  margin-bottom: 1rem;
  transition: transform 0.3s ease-in-out;
}

.logo:hover {
  transform: rotate(-5deg) scale(1.05);
}

.menu-header h1 {
  font-size: 2.4rem;
  margin: 0;
}

.menu-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background: linear-gradient(to right, #e8f5e9, #f1f8e9);
  width: 50%;
}

.menu-grid {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  width: 100%;
  max-width: 500px;
}

.menu-card {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 0.6rem 1rem;
  border-radius: 0.8rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  animation: fadeSlideUp 0.6s ease forwards;
  opacity: 0;
}

.menu-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.12);
}

.icon {
  font-size: 1.6rem;
  color: #019c54;
  margin-right: 0.8rem;
  transition: transform 0.3s ease;
}

.menu-card:hover .icon {
  animation: bounceIcon 0.6s ease-in-out;
}

.menu-card h2 {
  font-size: 1rem;
  margin: 0;
}

.btn {
  padding: 0.4rem 1rem;
  font-size: 1rem;
  border-radius: 1.2rem;
  background-color: #019c54;
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: background 0.3s, transform 0.2s, box-shadow 0.2s;
}

.btn:hover {
  background-color: #01693a;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.footer-text {
  text-align: center;
  font-size: 0.9rem;
  color: #555;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .menu-header {
    width: 100%;
    flex-direction: row;
    justify-content: center;
    padding: 1rem;
  }

  .menu-header .logo {
    width: 100px;
    margin-bottom: 0;
    margin-right: 1rem;
  }

  .menu-header h1 {
    font-size: 1.6rem;
  }

  .menu-section {
    width: 100%;
    padding: 1.5rem;
  }
}
</style>
