<template>
    <div class="weight-component">
      <b-card title="Registrar Peso">
        <!-- Campo para la fecha actual -->
        <b-form-group label="Fecha Actual">
          <b-form-input :value="currentDate" readonly></b-form-input>
        </b-form-group>
  
        <!-- Campo para ingresar la empacadora -->
        <b-form-group label="Empacadora">
          <b-form-input v-model="form.empacadora" placeholder="Ingresa la empacadora"></b-form-input>
        </b-form-group>
  
        <!-- Campo para ingresar el peso neto -->
        <b-form-group label="Peso Neto">
          <b-form-input v-model="form.pesoNeto" type="number" placeholder="Ingresa el peso neto"></b-form-input>
        </b-form-group>
  
        <!-- Campo para ingresar el formato -->
        <b-form-group label="Formato">
          <b-form-input v-model="form.formato" placeholder="Ingresa el formato"></b-form-input>
        </b-form-group>
  
        <!-- Campo para ingresar la marca -->
        <b-form-group label="Marca">
          <b-form-input v-model="form.marca" placeholder="Ingresa la marca"></b-form-input>
        </b-form-group>
  
        <!-- Campo para ingresar el lote -->
        <b-form-group label="Lote">
          <b-form-input v-model="form.lote" placeholder="Ingresa el lote"></b-form-input>
        </b-form-group>
  
        <!-- Campo para ingresar la fecha de fabricación -->
        <b-form-group label="Fecha de Fabricación">
          <b-form-input v-model="form.fechaFabricacion" type="date"></b-form-input>
        </b-form-group>
  
        <!-- Campo para ingresar la fecha de vencimiento -->
        <b-form-group label="Fecha de Vencimiento">
          <b-form-input v-model="form.fechaVencimiento" type="date"></b-form-input>
        </b-form-group>
  
        <!-- Botón de enviar -->
        <b-button variant="primary" @click="submitForm">Enviar</b-button>
      </b-card>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        // Almacenar los datos del formulario
        form: {
          empacadora: '',
          pesoNeto: '',
          formato: '',
          marca: '',
          lote: '',
          fechaFabricacion: '',
          fechaVencimiento: ''
        },
        currentDate: this.getCurrentDate() // Para mostrar la fecha actual
      };
    },
    methods: {
      // Obtener la fecha actual en formato DD/MM/YYYY
      getCurrentDate() {
        const today = new Date();
        const dd = String(today.getDate()).padStart(2, '0');
        const mm = String(today.getMonth() + 1).padStart(2, '0'); // Enero es 0
        const yyyy = today.getFullYear();
        return `${dd}/${mm}/${yyyy}`;
      },
      submitForm() {
        // Acción al enviar el formulario
        console.log("Formulario enviado:", this.form);
      }
    }
  };
  </script>
  
  <style scoped>
  .weight-component {
    max-width: 600px;
    margin: auto;
    padding: 20px;
  }
  </style>
  