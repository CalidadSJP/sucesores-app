<template>
  <div class="container mt-5">
    <h2 class="mb-4">Frecuencia de Inspección por Persona</h2>
    <div class="table-responsive">
      <input type="text" class="form-control mb-3" placeholder="Buscar por nombre o fecha..."
        v-model="searchQuery" />
      <table class="table">
        <thead>
          <tr>
            <th>Nombre del Operario</th>
            <th>Frecuencia de Inspección</th>
            <th>Última Inspección</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="frequencies.length === 0">
            <td colspan="3">No hay datos disponibles.</td>
          </tr>
          <tr v-for="frequency in filteredFrequencies" :key="frequency.nombre_operario">
            <td>{{ frequency.nombre_operario }}</td>
            <td>{{ frequency.frecuencia }}</td>
            <td>{{ frequency.ultima_inspeccion || 'N/A' }}</td>
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
      searchQuery: ''
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
          this.frequencies = response.data.sort((a, b) => a.frecuencia - b.frecuencia);
        } else {
          console.error('Formato inesperado de datos:', response.data);
        }
      } catch (error) {
        console.error('Error loading frequencies:', error.message);
        alert('Hubo un error al cargar los datos. Por favor, inténtalo de nuevo más tarde.');
      }
    },
  },
  computed: {
    filteredFrequencies() {
      const query = this.searchQuery.toLowerCase();
      return this.frequencies.filter(f =>
        f.nombre_operario.toLowerCase().includes(query) ||
        (f.ultima_inspeccion && f.ultima_inspeccion.toLowerCase().includes(query))
      );
    }
  },


};
</script>
