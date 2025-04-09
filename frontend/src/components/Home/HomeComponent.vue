<!-- src/components/HomeComponent.vue -->
<template>
  <div class="container mt-5">
    <div class="card text-center shadow">
      <div class="card-header">
        <h2>Sucesores App - Calidad</h2>
      </div>
      <div class="card-body">
        <p class="card-text">Seleccione una de las opciones:</p>
        <div class="d-grid gap-2 col-6 mx-auto">
          <router-link to="/control-home" class="btn btn-outline-primary">Personal</router-link>
          <router-link to="/additive-home" class="btn btn-outline-success">Ingreso Materia Prima/Material de
            Empaque/Aditivos</router-link>
          <router-link to="/weight" class="btn btn-outline-secondary">Control de Pesos</router-link>
          <!-- Se puede añadir más opciones aquí para futuras funcionalidades -->
          <!--<router-link to="/otra-opcion" class="btn btn-secondary">Otra Opción</router-link>-->
        </div>
      </div>
      <div class="card-footer text-muted">
        © 2024 Sucesores
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeComponent',
};
</script>

<style scoped>
.container {
  max-width: 600px;
}

.card-header {
  background-color: #019c54;
  color: white;
}

.btn-outline-success {
  border-color: #28a745;
  color: #28a745;
}

.btn-outline-primary {
  border-color: #007bff;
  color: #007bff;
}

.btn-outline-primary:hover,
.btn-outline-success:hover {
  color: white;
}

.card-footer {
  background-color: #f8f9fa;
}
</style>
