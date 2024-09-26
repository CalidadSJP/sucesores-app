<template>
    <div class="container mt-5">
      <div class="card">
        <div class="card-header">
          <h4>Registrar Peso</h4>
        </div>
        <div class="card-body">
          <!-- Fecha Actual -->
          <div class="mb-3">
            <label for="fecha" class="form-label">Fecha Actual</label>
            <input type="text" id="fecha" class="form-control" :value="currentDate" readonly>
          </div>
  
          <!-- Empacadora -->
          <div class="mb-3">
            <label for="empacadora" class="form-label">Empacadora</label>
            <input type="text" id="empacadora" class="form-control" v-model="form.empacadora">
          </div>
  
          <!-- Peso Neto -->
          <div class="mb-3">
            <label for="pesoNeto" class="form-label">Peso Neto</label>
            <input type="text" id="pesoNeto" class="form-control" v-model="form.pesoNeto">
          </div>
  
          <!-- Formato -->
          <div class="mb-3">
            <label for="formato" class="form-label">Formato</label>
            <input type="text" id="formato" class="form-control" v-model="form.formato">
          </div>
  
          <!-- Marca -->
          <div class="mb-3">
            <label for="marca" class="form-label">Marca</label>
            <input type="text" id="marca" class="form-control" v-model="form.marca">
          </div>
  
          <!-- Lote -->
          <div class="mb-3">
            <label for="lote" class="form-label">Lote</label>
            <input type="text" id="lote" class="form-control" v-model="form.lote">
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
  
          <!-- Botón de enviar -->
          <button class="btn btn-primary" @click="submitForm">Enviar</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        form: {
          empacadora: '',
          pesoNeto: '',
          formato: '',
          marca: '',
          lote: '',
          fechaFabricacion: '',
          fechaVencimiento: ''
        },
        currentDate: this.getCurrentDate()
      };
    },
    methods: {
      getCurrentDate() {
        const today = new Date();
        const day = String(today.getDate()).padStart(2, '0');
        const month = String(today.getMonth() + 1).padStart(2, '0'); // Meses empiezan desde 0
        const year = today.getFullYear();
        return `${day}/${month}/${year}`;
      },
      submitForm() {
        // Aquí puedes agregar la lógica para enviar el formulario
        console.log(this.form);
      }
    }
  };
  </script>
  
  <style scoped>
  /* Puedes agregar estilos adicionales si lo necesitas */
  </style>
  