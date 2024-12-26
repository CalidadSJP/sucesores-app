<template>
  <div class="container mt-5">
    <!-- Primera Tarjeta: Datos del Producto -->
    <div class="card mb-4">
      <div class="card-header d-flex align-items-center">
        <h4>Datos del Producto</h4>
        <!-- Botón para ir a HomeComponent con una imagen y texto -->
        <router-link to="/" class="back-link d-flex align-items-center ms-auto">
          <img src="@/assets/home.png" alt="Regresar" class="back-icon"
            style="width: 20px; height: 20px; margin-right: 5px;" />
          <span class="card-text">Inicio</span>
        </router-link>
      </div>
      <div class="card-body">
        <!-- Fecha Actual -->
        <div class="mb-3">
          <label for="fecha" class="form-label">Fecha</label>
          <input type="text" id="fecha" class="form-control" :value="currentDate" readonly>
        </div>

        <!-- EAN 13 -->
        <div class="mb-3">
          <label for="ean13" class="form-label">EAN 13</label>
          <input type="text" id="ean13" class="form-control uppercase-input" v-model="form.ean13">
        </div>

        <!-- EAN 14 -->
        <div class="mb-3">
          <label for="ean14" class="form-label">EAN 14</label>
          <input type="text" id="ean14" class="form-control uppercase-input" v-model="form.ean14">
        </div>

        <!-- Empacadora -->
        <div class="mb-3">
          <label for="empacadora" class="form-label">Empacadora</label>
          <input type="text" id="empacadora" class="form-control uppercase-input" v-model="form.empacadora">
        </div>

        <!-- Peso Neto -->
        <div class="mb-3">
          <label for="pesoNeto" class="form-label">Peso Neto</label>
          <input type="text" id="pesoNeto" class="form-control uppercase-input" v-model="form.pesoNeto">
        </div>

        <!-- Formato -->
        <div class="mb-3">
          <label for="formato" class="form-label">Formato</label>
          <input type="text" id="formato" class="form-control uppercase-input" v-model="form.formato">
        </div>

        <!-- Marca -->
        <div class="mb-3">
          <label for="marca" class="form-label">Marca</label>
          <input type="text" id="marca" class="form-control uppercase-input" v-model="form.marca">
        </div>

        <!-- Lote -->
        <div class="mb-3">
          <label for="lote" class="form-label">Lote</label>
          <input type="text" id="lote" class="form-control uppercase-input" v-model="form.lote">
        </div>

        <!-- Fecha de Fabricación -->
        <div class="mb-3">
          <label for="fechaFabricacion" class="form-label">Fecha de Fabricación</label>
          <input type="date" id="fechaFabricacion" class="form-control" v-model="form.fechaFabricacion">
        </div>

        <!-- Fecha de Vencimiento -->
        <div class="mb-3">
          <label for="fechaVencimiento" class="form-label">Fecha de Vencimiento</label>
          <input type="date" id="fechaVencimiento" class="form-control" v-model="form.fechaVencimiento">
        </div>
      </div>
    </div>

    <!-- Segunda Tarjeta: Pesos del Producto -->
    <div class="card mb-4">
      <div class="card-header">
        <h4>Pesos del Producto</h4>
      </div>
      <div class="card-body">
        <div class="row">
          <!-- Usamos una grilla de 5 columnas -->
          <div v-for="(peso, index) in form.pesos" :key="index" class="col-md-2 mb-3">
            <div class="input-group">
              <!-- Numeración a la izquierda -->
              <span class="input-group-text">{{ index + 1 }}</span>
              <!-- Añadimos min="0" para evitar pesos negativos -->
              <input type="number" class="form-control" v-model="form.pesos[index]" min="0" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Botón para enviar toda la información -->
    <div class="text-center">
      <button class="btn btn-primary w-100" @click="submitForm">Enviar Datos</button>
    </div><br><br><br>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentDate: new Date().toLocaleDateString('es-ES'),
      form: {
        empacadora: '',
        pesoNeto: '',
        formato: '',
        marca: '',
        lote: '',
        fechaFabricacion: '',
        fechaVencimiento: '',
        ean13: '',
        ean14: '',
        pesos: Array(30).fill('') // Array con 30 campos para pesos
      },
      imageSrc: require('@/assets/home.png'), // Ruta de la imagen
    };
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    submitForm() {
      // Validación para asegurarse de que los pesos no sean negativos
      if (this.form.pesos.some(peso => peso < 0)) {
        alert('Los pesos no pueden ser negativos');
        return;
      }
      // Lógica para enviar todos los datos del formulario
      console.log(this.form);
    }
  }
};
</script>

<style scoped>
.uppercase-input {
  text-transform: uppercase;
}

/* Estilo adicional si es necesario */
.back-link {
  text-decoration: none;
}

.back-icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}

.card-text {
  font-size: 23px;
  /* Ajusta el tamaño de la palabra según sea necesario */
  color: #000;
  /* Ajusta el color de la palabra según sea necesario */

}
</style>