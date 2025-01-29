<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header d-flex align-items-center">
            <!-- Logo al lado del título -->
            <img src="@/assets/sucesores-logo-1.png" alt="Logo" class="logo"
              style="width: 135px; height: 90px; margin-right: 0px;" />
            <h1 class="mb-0">Control de Practicas del Personal</h1>
          </div>
          <div class="card-body">
            <form @submit.prevent="submitForm">
              <!-- Encabezado -->
              <router-link to="/control-home" class="back-link">
                <img src="@/assets/home.png" alt="Regresar" class="back-icon" />
                <span class="card-text">Inicio</span>
              </router-link><br><br>
              <router-link to="/frecuency" class="frequency-link">
                <img src="@/assets/frecuencia.png" alt="Regresar" class="back-icon" />
                <span class="card-text">Frecuencia de inspección</span>
              </router-link>
              <br>
              <div class="form-group">
                <label for="fecha">Fecha:</label>
                <input type="date" id="fecha" class="form-control" v-model="form.fecha" required />
              </div>

              <div class="form-group">
                <label for="turno">Turno:</label>
                <select id="turno" class="form-control" v-model="form.turno" required>
                  <option value="I">I</option>
                  <option value="II">II</option>
                  <option value="III">III</option>
                </select>
              </div>

              <div class="form-group">
                <label for="area">Área:</label>
                <select id="area" class="form-control" v-model="form.area" @change="filterOperarios" required>
                  <option disabled value=""></option>
                  <option v-for="area in areaNames" :key="area.id_area" :value="area.id_area">
                    {{ area.name_area }}
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label for="nombre_operario">Operario:</label>
                <select id="nombre_operario" class="form-control" v-model="form.nombre_operario" required>
                  <option disabled value=""></option>
                  <option v-for="name in filteredOperarios" :key="name" :value="name">
                    {{ name }}
                  </option>
                </select>
              </div>
              <br /><br />

              <!-- Cuerpo del formulario -->
              <fieldset class="form-group">
                <div class="d-flex align-items-center">
                  <img src="@/assets/check.png" alt="Logo" class="logo"
                    style="width: 65px; height: 65px; margin-right: 10px; padding: 15px; vertical-align: middle;" />
                  <h2 class="mb-0">Inspección</h2>
                </div>
                <br /><br />

                <div v-for="item in items" :key="item.name" class="form-group">
                  <label :for="item.name">{{ item.label }}</label>
                  <select class="form-control" :id="item.name" v-model="form[item.name]">
                    <option v-for="option in item.options" :key="option" :value="option">
                      {{ option }}
                    </option>
                  </select>
                </div>
              </fieldset>

              <!-- Pie de página -->
              <div class="form-group">
                <label for="supervisor">Supervisor:</label>
                <select id="supervisor" class="form-control" v-model="form.supervisor" required>
                  <option v-for="name in supervisorNames" :key="name" :value="name">
                    {{ name }}
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label for="observaciones">Observaciones:</label>
                <textarea id="observaciones" class="form-control" v-model="form.observaciones" rows="3"></textarea>
              </div>
              <br />
              <div class="form-buttons">
                <button type="submit" class="btn btn-success w-50" :disabled="isLoading">
                  <!-- Mostrar spinner dentro del botón -->
                  <span v-if="isLoading" class="spinner-border spinner-border-sm mr-2" role="status"
                    aria-hidden="true"></span>
                  {{ isLoading ? 'Guardando...' : 'Enviar' }}
                </button>
                <button @click.prevent="scrollToTop" class="btn btn-secondary scroll-to-top w-50">
                  Regresar
                </button>
              </div>
              <br>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "FormComponent",
  data() {
    return {
      isLoading: false,
      form: {
        fecha: "",
        turno: "",
        area: "",
        nombre_operario: "",
        manos_limpias: "",
        uniforme_limpio: "",
        no_objetos_personales: "",
        heridas_protegidas: "",
        cofia_bien_puesta: "",
        mascarilla_bien_colocada: "",
        protector_auditivo: "",
        unas_cortas: "",
        guantes_limpios: "",
        pestanas: "",
        barba_bigote: "",
        medicamento_autorizado: "",
        supervisor: "",
        observaciones: "",
      },
      items: [
        { name: "manos_limpias", label: "Manos limpias", options: ["Cumple", "No cumple"] },
        { name: "uniforme_limpio", label: "Uniforme limpio", options: ["Cumple", "No cumple"] },
        { name: "no_objetos_personales", label: "No objetos personales en el área", options: ["Cumple", "No cumple", "No aplica"] },
        { name: "heridas_protegidas", label: "Presenta heridas protegidas", options: ["Cumple", "No cumple", "No aplica"] },
        { name: "cofia_bien_puesta", label: "Cofia bien puesta", options: ["Cumple", "No cumple"] },
        { name: "mascarilla_bien_colocada", label: "Mascarilla bien colocada", options: ["Cumple", "No cumple"] },
        { name: "protector_auditivo", label: "Uso de protector auditivo", options: ["Cumple", "No cumple", "No aplica"] },
        { name: "unas_cortas", label: "Uñas Cortas, limpias y sin esmalte", options: ["Cumple", "No cumple"] },
        { name: "guantes_limpios", label: "Guantes limpios y en buen estado", options: ["Cumple", "No cumple", "No aplica"] },
        { name: "pestanas", label: "Pestañas sin rímel o extensiones", options: ["Cumple", "No cumple", "No aplica"] },
        { name: "barba_bigote", label: "Barba/Bigote", options: ["Cumple", "No cumple", "No aplica"] },
        { name: "medicamento_autorizado", label: "Uso de medicamento con autorización del supervisor", options: ["Cumple", "No cumple", "No aplica"] },
      ],
      operarioNames: [],
      supervisorNames: [],
      areaNames: [],
      personnel: [], // Guarda los datos del personal completo, incluyendo el id_area
      filteredOperarios: [], // Variable para filtrar operarios según el área seleccionada
    };
  },
  async created() {
    await this.loadPersonnel();
    await this.loadAreas();
  },
  methods: {
    async loadPersonnel() {
      this.isLoading = true;
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-personnel`);
        const personnelData = response.data.personnel || []; // Accede al arreglo dentro de 'personnel'

        // Verificamos si personnelData es un arreglo
        if (!Array.isArray(personnelData)) {
          throw new Error("La respuesta no es un arreglo");
        }

        // Convertimos el arreglo de arreglos a un arreglo de objetos
        this.personnel = personnelData.map(item => ({
          id: item[0],
          nombre: item[1],
          role: item[2],
          id_area: item[3]
        }));

        // Extraemos los nombres para los selects
        this.operarioNames = this.personnel.map(person => ({ name: person.nombre, id_area: person.id_area }));
        this.supervisorNames = this.personnel
          .filter(person => person.role.startsWith('SUPERVISOR'))
          .map(person => person.nombre);
      } catch (error) {
        console.error("Error al cargar el personal:", error);
        alert("Hubo un error al cargar el personal. Por favor, inténtelo de nuevo.");
      } finally {
        this.isLoading = false;
      }
    },
    async loadAreas() {
      this.isLoading = true;
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-areas`);
        // Acceder correctamente al arreglo de áreas
        this.areaNames = response.data.areas.map(area => ({ id_area: area[0], name_area: area[1] })) || [];
      } catch (error) {
        console.error("Error al cargar áreas:", error);
      } finally {
        this.isLoading = false;
      }
    },
    filterOperarios() {
      const selectedArea = this.form.area;
      if (selectedArea) {
        this.filteredOperarios = this.operarioNames
          .filter(person => person.id_area === selectedArea)
          .map(person => person.name);
      } else {
        this.filteredOperarios = this.operarioNames.map(person => person.name);
      }
    },
    async submitForm() {
      this.isLoading = true;
      try {
        // Copia el formulario actual
        const formToSubmit = { ...this.form };

        // Validar que areaNames contenga el área seleccionada
        const selectedArea = this.areaNames.find(a => a.id_area === formToSubmit.area);
        if (!selectedArea) {
          throw new Error("Área seleccionada no válida.");
        }

        // Asignar el nombre del área al formulario
        formToSubmit.area = selectedArea.name_area;

        // Hacer la solicitud POST al backend (ajustado para que coincida con la ruta del backend)
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/api/submit-form`, // Ajustado si no usas "/api" en tu ruta
          formToSubmit
        );

        // Verificar si la respuesta es exitosa
        if (response.data && response.data.message) {
          alert(response.data.message);
        } else {
          alert("Formulario guardado exitosamente");
        }

        // Reiniciar el formulario después de guardar
        this.resetForm();

      } catch (error) {
        console.error("Error al guardar el formulario:", error);

        // Manejar el mensaje de error
        const errorMessage = error.response?.data?.error || "Hubo un error al guardar el formulario. Por favor, inténtelo de nuevo.";
        alert(errorMessage);

      } finally {
        this.isLoading = false; // Detener la animación de carga
      }
    },

    resetForm() {
      this.form = {
        fecha: "",
        turno: "",
        area: "",
        nombre_operario: "",
        manos_limpias: "",
        uniforme_limpio: "",
        no_objetos_personales: "",
        heridas_protegidas: "",
        cofia_bien_puesta: "",
        mascarilla_bien_colocada: "",
        protector_auditivo: "",
        unas_cortas: "",
        guantes_limpios: "",
        pestanas: "",
        barba_bigote: "",
        medicamento_autorizado: "",
        supervisor: "",
        observaciones: "",
      };
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
  },
};
</script>



<style scoped>
.page-container {
  background-color: #007940;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.card {
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

textarea {
  resize: vertical;
}

.card-body {
  position: relative;
  padding: 20px;
}

.back-icon {
  width: 25px;
  /* Ajusta el ancho del ícono */
  height: 25px;
  /* Ajusta la altura del ícono */
  margin-right: 8px;
}

.back-link {
  position: absolute;
  top: 20px;
  /* Ajusta según sea necesario */
  left: 20px;
  /* Ajusta según sea necesario */
  display: flex;
  align-items: center;
  /* Otros estilos para el enlace, como padding o margin */
  text-decoration: none;
  /* Elimina el subrayado del enlace */
}

.frequency-link {
  display: flex;
  align-items: center;
  /* Otros estilos para el enlace, como padding o margin */
  text-decoration: none;
  /* Elimina el subrayado del enlace */
}

.card-text {
  font-size: 23px;
  /* Ajusta el tamaño de la palabra según sea necesario */
  color: #000;
  /* Ajusta el color de la palabra según sea necesario */

}

.form-buttons {
  margin-top: 20px;
  /* Espacio superior entre el formulario y los botones */
  display: flex;
  /* Muestra los botones en una fila */
  gap: 10px;
  /* Espacio entre los botones */
  justify-content: flex-start;
  /* Alinea los botones a la izquierda */
}
</style>
