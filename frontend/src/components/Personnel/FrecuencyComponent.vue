<template>
  <div class="container mt-5">
    <h2 class="mb-4">Frecuencia de Inspección por Persona</h2>

    <div class="card shadow-sm">
      <div class="card-body">
        <!-- Filtros -->
        <div class="row mb-3">
          <div class="col-md-6 mb-1">
            <input type="text" class="form-control" placeholder="Buscar por nombre" v-model="filters.nombre" />
          </div>

          <div class="col-md-6 mb-1">
            <input type="text" class="form-control" placeholder="Buscar por area" v-model="filters.area" />
          </div>

          <div class="col-md-6 mb-1">
            <input type="number" class="form-control" placeholder="Frecuencia mínima"
              v-model.number="filters.frecuenciaMin" />
          </div>
          <div class="col-md-6 mb-1">
            <input type="number" class="form-control" placeholder="Frecuencia máxima"
              v-model.number="filters.frecuenciaMax" />
          </div>
        </div>

        <div class="row mb-4">
          <div class="col-md-6 mb-2">
            <label class="form-label">Desde:</label>
            <input type="date" class="form-control" v-model="filters.fechaDesde" />
          </div>
          <div class="col-md-6 mb-2">
            <label class="form-label">Hasta:</label>
            <input type="date" class="form-control" v-model="filters.fechaHasta" />
          </div>
        </div>

        <!-- Tabla de resultados -->
        <div class="table-responsive">
          <table class="table table-bordered table-striped">
            <thead class="table-dark">
              <tr>
                <th>Nombre del Operario</th>
                <th>Área</th>
                <th>Frecuencia de Inspección</th>
                <th>Última Inspección</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredFrequencies.length === 0">
                <td colspan="3" class="text-center">No hay datos disponibles.</td>
              </tr>
              <tr v-for="frequency in filteredFrequencies" :key="frequency.nombre_operario">
                <td>{{ frequency.nombre_operario }}</td>
                <td>{{ frequency.area }}</td>
                <td>{{ frequency.frecuencia }}</td>
                <td>{{ frequency.ultima_inspeccion || 'N/A' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      frequencies: [],
      filters: {
        nombre: '',
        area: '',
        frecuenciaMin: null,
        frecuenciaMax: null,
        fechaDesde: '',
        fechaHasta: ''
      }
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
        console.error('Error al cargar frecuencias:', error.message);
        alert('Error al cargar los datos.');
      }
    },
  },
  computed: {
    filteredFrequencies() {
      return this.frequencies.filter(f => {
        // Filtro por nombre (evita errores con null o undefined)
        const nombreMatch = (f.nombre_operario || '')
          .toLowerCase()
          .includes((this.filters.nombre || '').toLowerCase());

          // Filtro por nombre (evita errores con null o undefined)
        const areaMatch = (f.area || '')
          .toLowerCase()
          .includes((this.filters.area || '').toLowerCase());

        // Filtro por frecuencia
        const min = this.filters.frecuenciaMin;
        const max = this.filters.frecuenciaMax;
        const frecuenciaMatch =
          (min === null || min === '' || f.frecuencia >= Number(min)) &&
          (max === null || max === '' || f.frecuencia <= Number(max));

        // Filtro por fecha
        const fechaRaw = f.ultima_inspeccion;
        let fechaValida = true;

        if (fechaRaw) {
          const fecha = new Date(fechaRaw);
          const desde = this.filters.fechaDesde ? new Date(this.filters.fechaDesde) : null;
          const hasta = this.filters.fechaHasta ? new Date(this.filters.fechaHasta) : null;

          if (desde && fecha < desde) fechaValida = false;
          if (hasta && fecha > hasta) fechaValida = false;
        } else {
          if (this.filters.fechaDesde || this.filters.fechaHasta) fechaValida = false;
        }

        return nombreMatch && frecuenciaMatch && fechaValida && areaMatch;
      });
    }

  }



};
</script>
