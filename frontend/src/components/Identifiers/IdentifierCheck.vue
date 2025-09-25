<template>
  <div class="container mt-4">
    <h2 class="mb-3 text-center">Lectura de Cédula Ecuatoriana</h2>

    <!-- Subida de imagen -->
    <div class="card p-3 mb-4 shadow-sm">
      <label class="form-label">Tomar foto o seleccionar imagen</label>
      <input type="file" accept="image/*" @change="onFileChange" />
      <button
        class="btn btn-success w-100"
        :disabled="!selectedFile"
        @click="processCedula"
      >
        Obtener datos de la cédula
      </button>

      <!-- Preview de la imagen -->
      <div v-if="previewUrl" class="mt-3 text-center">
        <img :src="previewUrl" alt="Preview cédula" class="img-fluid" style="max-height: 300px; border:1px solid #ccc;"/>
      </div>
    </div>

    <!-- Formulario autollenado -->
    <div class="card p-4 shadow-sm">
      <h5 class="mb-3">Datos extraídos</h5>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label class="form-label">Cédula</label>
          <input v-model="form.cedula" type="text" class="form-control" readonly />
        </div>
        <div class="mb-3">
          <label class="form-label">Apellido(s)</label>
          <input v-model="form.apellido" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Nombre(s)</label>
          <input v-model="form.nombre" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Fecha de Nacimiento</label>
          <input v-model="form.fecha_nacimiento" type="text" class="form-control" />
        </div>

        <button type="submit" class="btn btn-primary w-100">Guardar</button>
      </form>
    </div>

    <!-- Debug (opcional) -->
    <div v-if="debug.length" class="card p-3 mt-4">
      <h6>Texto OCR detectado (debug)</h6>
      <ul>
        <li v-for="(line, i) in debug" :key="i">{{ line }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";

export default {
  name: "CedulaForm",
  setup() {
    const form = ref({
      cedula: "",
      apellido: "",
      nombre: "",
      fecha_nacimiento: "",
    });

    const debug = ref([]);
    const selectedFile = ref(null);
    const previewUrl = ref(null);

    const uploadCedula = async (file) => {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/api/upload-id`,
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );

        const data = response.data;
        console.log("Respuesta OCR:", data);

        form.value.cedula = data.cedula || "";
        form.value.apellido = data.apellido || "";
        form.value.nombre = data.nombre || "";
        form.value.fecha_nacimiento = data.fecha_nacimiento || "";
        debug.value = data.ocr_debug || [];
      } catch (error) {
        console.error("Error subiendo cédula:", error);
        alert("No se pudo procesar la cédula");
      }
    };

    const onFileChange = (event) => {
      selectedFile.value = event.target.files[0];

      if (selectedFile.value) {
        // Generar preview
        previewUrl.value = URL.createObjectURL(selectedFile.value);
      } else {
        previewUrl.value = null;
      }
    };

    const processCedula = async () => {
      if (!selectedFile.value) {
        alert("Primero selecciona una foto de la cédula");
        return;
      }
      await uploadCedula(selectedFile.value);
    };

    const submitForm = async () => {
      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/api/save-cedula`,
          form.value
        );
        console.log("Formulario guardado:", response.data);
        alert("Datos guardados correctamente");
      } catch (error) {
        console.error("Error guardando formulario:", error);
        alert("No se pudo guardar el formulario");
      }
    };

    return {
      form,
      debug,
      selectedFile,
      previewUrl,
      onFileChange,
      processCedula,
      submitForm,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
