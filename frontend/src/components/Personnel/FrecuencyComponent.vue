<template>
  <div class="container mt-5">
    <!-- Mostrar frecuencia de inspección -->
    <h2 class="mb-4">Frecuencia de Inspección por Persona</h2>
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th>Nombre del Operario</th>
            <th>Frecuencia de Inspección</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="frequencies.length === 0">
            <td colspan="2">No hay datos disponibles.</td>
          </tr>
          <tr v-for="frequency in frequencies" :key="frequency.nombre_operario">
            <td>{{ frequency.nombre_operario }}</td>
            <td>{{ frequency.frecuencia }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  data() {
    return {
      frequencies: [],
    };
  },
  async created() {
    await this.loadFrequencies();
  },
  methods: {
    async loadFrequencies() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/inspection-frequency`);

        if (response.data && Array.isArray(response.data)) {
          // Ordenar por frecuencia ascendente
          this.frequencies = response.data.sort((a, b) => a.frecuencia - b.frecuencia);
        } else {
          console.error('Formato inesperado de datos:', response.data);
        }
      } catch (error) {
        console.error('Error loading frequencies:', error.message);
        alert('Hubo un error al cargar los datos. Por favor, inténtalo de nuevo más tarde.');
      }
    }

  }
};
</script>
