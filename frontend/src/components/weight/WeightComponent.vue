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

        <!-- EAN 14 
        <div class="mb-3">
          <label for="ean14" class="form-label">EAN 14</label>
          <input type="text" id="ean14" class="form-control uppercase-input" v-model="form.ean14">
        </div> -->

        <!-- Empacadora -->
        <div class="mb-3">
          <label for="empacadora" class="form-label">Empacadora</label>
          <select id="empacadora" class="form-control" v-model="form.empacadora" required>
            <option value="">Seleccione una empacadora</option>
            <option v-for="baler in empacadoras" :key="baler.id" :value="baler.baler_name">
              {{ baler.baler_name }}
            </option>
          </select>
        </div>


        <!-- Peso Neto -->
        <div class="mb-3">
          <label for="pesoNeto" class="form-label">Peso Neto</label>
          <input type="number" placeholder="1.0" step="0.01" min="0" max="100000" id="pesoNeto"
            class="form-control uppercase-input" v-model="form.pesoNeto">
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
    <div class="card mb-4 card-large">
      <div class="card-header bg-success text-white">
        <h4 class="m-0 d-flex align-items-center">
          <i class="fas fa-weight-hanging me-2"></i> Pesos del Producto
        </h4>
      </div>

      <div class="card-body">
        <div class="row">
          <!-- Usamos una grilla de 5 columnas -->
          <div v-for="(peso, index) in form.pesos" :key="index" class="col-md-2 mb-3">
            <div class="input-group">
              <!-- Numeración a la izquierda -->
              <span class="input-group-text">{{ index + 1 }}</span>
              <!-- Añadimos min="0" para evitar pesos negativos -->
              <input type="number" step="0.01" max="100000" class="form-control" v-model="form.pesos[index]" min="0" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Botón para enviar toda la información -->
    <div class="d-flex justify-content-end m-0 p-0">
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
      currentDate: new Date().toISOString().split('T')[0], // Formato YYYY-MM-DD
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
      fetchTimeout: null, // Para controlar el tiempo de espera
      empacadoras: []
    };
  },
  watch: {
    // Observar cambios en el campo 'ean13'
    'form.ean13': function (newEAN13) {
      if (newEAN13) {
        this.fetchProductInfo(); // Llamar al método cuando cambie el ean13
      }
    },
    'form.fechaFabricacion'(newFecha) {
      if (newFecha) {
        let fecha = new Date(newFecha);
        fecha.setFullYear(fecha.getFullYear() + 1); // Sumar un año
        this.form.fechaVencimiento = fecha.toISOString().split('T')[0]; // Formato YYYY-MM-DD
      } else {
        this.form.fechaVencimiento = ''; // Vaciar si no hay fecha de fabricación
      }
    }
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    async fetchProductInfo() {

      // Limpiar el timeout previo para evitar llamadas innecesarias
      if (this.fetchTimeout) {
        clearTimeout(this.fetchTimeout);
      }

      // Esperar 500ms después de que el usuario deje de escribir antes de hacer la solicitud
      this.fetchTimeout = setTimeout(async () => {
        try {
          const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-product-info`, {
            params: { ean13: this.form.ean13 }
          });

          if (response.status === 200) {
            const data = response.data;
            this.form.ean14 = data.ean14;
            this.form.pesoNeto = data.peso_neto;
            this.form.formato = data.formato;
            this.form.marca = data.marca;
          } else {
            console.warn(response.data.error || 'No se encontró el producto');
          }
        } catch (error) {
          console.error("Error al obtener la información:", error);
        }
      }, 500);
    },
    async fetchBalers() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-balers`);
        if (response.status === 200) {
          this.empacadoras = response.data;
        } else {
          console.warn("No se pudieron cargar las empacadoras");
        }
      } catch (error) {
        console.error("Error al obtener las empacadoras:", error);
      }
    },
    async submitForm() {
      // Validar que los pesos no sean negativos
      if (this.form.pesos.some(peso => peso < 0)) {
        alert('Los pesos no pueden ser negativos');
        return;
      }

      // Construir el objeto con los datos a enviar
      const payload = {
        date: this.currentDate, // Fecha actual
        baler: this.form.empacadora.toUpperCase(), // Nombre de la empacadora
        net_weight: this.form.pesoNeto, // Peso neto
        format: this.form.formato.toUpperCase(), // Formato
        brand: this.form.marca.toUpperCase(), // Marca
        lot: this.form.lote.toUpperCase(), // Lote
        ean13: this.form.ean13,
        manufacture_date: this.form.fechaFabricacion, // Fecha de fabricación
        expiry_date: this.form.fechaVencimiento, // Fecha de vencimiento
        weights: this.form.pesos.map(p => (p !== "" ? parseFloat(p) : null)) // Convertir pesos a números, dejando NULL los vacíos
      };

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/api/save-weight-control`,
          payload
        );

        if (response.status === 201) {
          alert('Registro guardado exitosamente');
          this.resetForm(); // Reiniciar el formulario después de guardar
          this.$router.push('/weight-resume');
        } else {
          alert('Error al guardar los datos');
        }
      } catch (error) {
        console.error("Error al enviar los datos:", error);
        alert('Error al conectar con el servidor');
      }
    },
    resetForm() {
      this.form = {
        empacadora: '',
        pesoNeto: '',
        formato: '',
        marca: '',
        lote: '',
        fechaFabricacion: '',
        fechaVencimiento: '',
        ean13: '',
        ean14: '',
        pesos: Array(30).fill('') // Reiniciar los pesos
      };
    }
  },
  mounted() {
    this.fetchBalers(); // Cargar empacadoras al iniciar el componente
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

.custom-back-button {
  display: flex;
  /* Activa flexbox para alinear elementos */
  align-items: center;
  /* Alinea verticalmente ícono y texto */
  justify-content: center;
  /* Centra contenido horizontalmente dentro del botón */
  background-color: #ffffff;
  /* Cambia al color deseado */
  color: rgb(0, 0, 0);
  /* Texto negro */
  border: none;
  /* Elimina bordes */
  border-radius: 8px;
  /* Bordes redondeados */
  padding: 10px 20px;
  /* Añade espaciado interno */
  font-size: 16px;
  /* Tamaño del texto */
  font-weight: bold;
  /* Hace el texto más visible */
  cursor: pointer;
  /* Cambia el cursor al pasar sobre el botón */
  gap: 10px;
  /* Espaciado entre el ícono y el texto */
  transition: background-color 0.3s;
  /* Animación al cambiar color */
}

.custom-register-button {
  display: flex;
  /* Activa flexbox para alinear elementos */
  align-items: center;
  /* Alinea verticalmente ícono y texto */
  justify-content: center;
  /* Centra contenido horizontalmente dentro del botón */
  background-color: #ffffff;
  /* Cambia al color deseado */
  color: rgb(0, 0, 0);
  /* Texto negro */
  border: none;
  /* Elimina bordes */
  border-radius: 8px;
  /* Bordes redondeados */
  padding: 10px 20px;
  /* Añade espaciado interno */
  font-size: 16px;
  /* Tamaño del texto */
  font-weight: bold;
  /* Hace el texto más visible */
  cursor: pointer;
  /* Cambia el cursor al pasar sobre el botón */
  gap: 10px;
  /* Espaciado entre el ícono y el texto */
  transition: background-color 0.3s;
  /* Animación al cambiar color */
}


/* Cambia el color al pasar el mouse */
.custom-back-button:hover {
  background-color: #e3e6e9;
  /* Cambia ligeramente el color */
}

/* Estilo para el ícono */
.button-icon {
  width: 22px;
  /* Tamaño del ícono */
  height: 22px;
  /* Tamaño del ícono */
}

.card-text {
  font-size: 23px;
  /* Ajusta el tamaño de la palabra según sea necesario */
  color: #000;
  /* Ajusta el color de la palabra según sea necesario */

}

.card-large {
  max-width: 1000px;
  /* Limitar el contenedor a 1000px en pantallas grandes */
  width: 100%;
  /* El contenedor ocupa el 100% del ancho disponible */
  margin: 0 auto;
  /* Centra el contenedor */
}

.container {
  max-width: 1000px;
  /* Limitar el ancho del contenedor a 1000px */
  padding-left: 15px;
  /* Asegurarse de que haya un pequeño espacio en los lados */
  padding-right: 15px;
}

.d-flex.justify-content-end {
  margin-right: 0;
  /* Asegura que no haya margen derecho */
  padding-right: 0;
  /* Elimina el padding derecho */
}

.custom-flat-button {
  background: transparent;
  border: none;
  padding: 0;
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 2px;
  cursor: pointer;
  box-shadow: none;
  transition: none;
}

/* Elimina cualquier efecto hover */
.custom-flat-button:hover {
  background: transparent;
  color: inherit;
}

.custom-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  padding: 20px;
}

.button-group {
  display: flex;
  gap: 20px;
  margin-left: auto;
  /* Empuja el grupo a la derecha */
}
</style>