<template>
  <div class="container mt-5">
    <!-- Primera Tarjeta: Datos del Producto -->
    <div class="card mb-4 card-large">
      <div class="card-header d-flex bg-success text-white custom-header align-items-center">
        <h4 class="m-0 d-flex align-items-center">
          <i class="fas fa-database me-2"></i> Datos
        </h4>

        <div class="button-group">
          <button @click="$router.push('/')" class="custom-flat-button text-white">
            <i class="fas fa-home me-1"></i> Inicio
          </button>
          <button @click="$router.push('/weight-register')" class="custom-flat-button text-white">
            <i class="fas fa-clipboard-list me-1"></i> Registro
          </button>
        </div>
      </div>

      <div class="card-body">
        <div class="row">
          <!-- Fecha -->
          <div class="col-md-6 mb-3">
            <label class="form-label">Fecha</label>
            <input type="text" class="form-control" :value="currentDate" readonly>
          </div>

          <!-- Peso Neto -->
          <div class="col-md-6 mb-3">
            <label class="form-label">Peso Neto</label>
            <select class="form-control" v-model="form.pesoNeto" required>
              <option value="">Seleccione peso</option>
              <option value="50">50 KG</option>
              <option value="25">25 KG</option>
              <option value="9">9 KG</option>
            </select>
          </div>

          <!-- Marca -->
          <div class="col-md-6 mb-3">
            <label class="form-label">Marca</label>
            <input type="text" class="form-control uppercase-input" v-model="form.marca" required>
          </div>

          <!-- Lote -->
          <div class="col-md-6 mb-3">
            <label class="form-label">Lote</label>
            <input type="text" class="form-control uppercase-input" v-model="form.lote" required>
          </div>

          <!-- Fecha Fabricación -->
          <div class="col-md-6 mb-3">
            <label class="form-label">Fecha de Fabricación</label>
            <input type="date" class="form-control" v-model="form.fechaFabricacion" required>
          </div>

          <!-- Fecha Vencimiento -->
          <div class="col-md-6 mb-3">
            <label class="form-label">Fecha de Vencimiento</label>
            <input type="date" class="form-control" v-model="form.fechaVencimiento" readonly>
          </div>

          <!-- Responsable de Empaque -->
          <div class="mb-3">
            <label for="packagingResponsible" class="form-label">
              Responsable de Empaque
            </label>
            <input type="text" id="packagingResponsible" class="form-control uppercase-input"
              v-model="form.packagingResponsible" required>
          </div>

        </div>
      </div>

    </div>

    <!-- Segunda Tarjeta: Pesos del Producto -->
    <div v-if="form.pesoNeto" class="card mb-4 card-large">
      <div class="card-header bg-success text-white">
        <h4 class="m-0 d-flex align-items-center">
          <i class="fas fa-weight-hanging me-2"></i> Pesos del Producto
        </h4>
      </div>

      <div class="card-body">
        <!-- Pesos principales (30) -->
        <h6 class="fw-bold mb-2">Pesos principales</h6>
        <div class="row">
          <div v-for="(peso, index) in primaryWeights" :key="'p-' + index" class="col-md-2 mb-3">
            <div class="input-group">
              <span class="input-group-text">{{ index + 1 }}</span>
              <input type="number" step="0.01" min="0" class="form-control" v-model.number="primaryWeights[index]" />
            </div>
          </div>
        </div>

        <!-- Pesos adicionales SOLO para 50 KG -->
        <div v-if="form.pesoNeto === '50'">
          <hr><br>
          <h6 class="fw-bold mb-2">Pesos adicionales</h6>
          <div class="row">
            <div v-for="(peso, index) in secondaryWeights" :key="'s-' + index" class="col-md-2 mb-3">
              <div class="input-group">
                <span class="input-group-text">{{ index + 1 }}</span>
                <input type="number" step="0.01" min="0" class="form-control" v-model="secondaryWeights[index]" />
              </div>
            </div>
          </div>
        </div>
      </div>


    </div>

    <!-- Botón Enviar -->
    <div class="d-flex justify-content-end">
      <button class="btn btn-primary" @click="submitForm">
        <i class="fas fa-save"></i> Enviar datos
      </button>
    </div>

    <br><br><br>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      currentDate: new Date().toISOString().split('T')[0],
      form: {
        pesoNeto: '',
        marca: '',
        lote: '',
        packagingResponsible: '',
        fechaFabricacion: '',
        fechaVencimiento: ''
      },
      primaryWeights: Array(30).fill(''),
      secondaryWeights: []
    };
  },


  watch: {
    'form.pesoNeto'(value) {
      if (value === '9') {
        this.primaryWeights = Array(30).fill('');
        this.secondaryWeights = [];
      }

      if (value === '50') {
        this.primaryWeights = Array(30).fill('');
        this.secondaryWeights = Array(10).fill('');
      }

      if (value === '25') {
        // Se define después
        this.primaryWeights = [];
        this.secondaryWeights = [];
      }
    },

    'form.fechaFabricacion'(newFecha) {
      if (newFecha) {
        const fecha = new Date(newFecha);
        fecha.setFullYear(fecha.getFullYear() + 1);
        this.form.fechaVencimiento = fecha.toISOString().split('T')[0];
      } else {
        this.form.fechaVencimiento = '';
      }
    }
  },


  methods: {
    async submitForm() {
      const allWeights = [
        ...this.primaryWeights,
        ...this.secondaryWeights
      ];

      if (allWeights.some(p => p !== '' && p < 0)) {
        alert('Los pesos no pueden ser negativos');
        return;
      }


      const payload = {
        date: this.currentDate,
        net_weight: this.form.pesoNeto,
        brand: this.form.marca.toUpperCase(),
        lot: this.form.lote.toUpperCase(),
        packaging_responsible: this.form.packagingResponsible.toUpperCase(),
        manufacture_date: this.form.fechaFabricacion,
        expiry_date: this.form.fechaVencimiento,
        primary_weights: this.primaryWeights.map(p => (p !== '' ? parseFloat(p) : null)),
        secondary_weights: this.secondaryWeights.map(p => (p !== '' ? parseFloat(p) : null))
      };



      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/api/save-weight-control-B1`,
          payload
        );

        if (response.status === 201) {
          alert('Registro guardado exitosamente');
          this.resetForm();
        } else {
          alert('Error al guardar los datos');
        }
      } catch (error) {
        console.error(error);
        alert('Error al conectar con el servidor');
      }
    },

    resetForm() {
      this.form = {
        pesoNeto: '',
        marca: '',
        lote: '',
        packagingResponsible: '',
        fechaFabricacion: '',
        fechaVencimiento: ''
      };
      this.primaryWeights = Array(30).fill('');
      this.secondaryWeights = [];
    }

  }
};
</script>

<style scoped>
.uppercase-input {
  text-transform: uppercase;
}

.card-large {
  max-width: 1000px;
  margin: 0 auto;
}

.container {
  max-width: 1000px;
}

.custom-flat-button {
  background: transparent;
  border: none;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

.custom-header {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}

.button-group {
  display: flex;
  gap: 20px;
}
</style>
