<template>
  <div class="container mt-4">
    
    <!-- TARJETA DE EXPORTACIÓN -->
    <div class="card shadow-sm rounded mb-3">
      <div class="card-body p-3">
        <h5 class="card-title mb-3">Exportar Registros del Mes</h5>
        <div class="row">
          <div class="col-md-6 mb-2">
            <select v-model="selectedMonth" class="form-control" required>
              <option disabled value="">Seleccione Mes</option>
              <option v-for="(name, index) in months" :key="index" :value="index + 1">{{ name }}</option>
            </select>
          </div>
          <div class="col-md-6 mb-2">
            <select v-model="selectedYear" class="form-control" required>
              <option disabled value="">Seleccione Año</option>
              <option v-for="year in years" :key="year">{{ year }}</option>
            </select>
          </div>
        </div>
        <button
          class="btn btn-outline-primary btn-sm w-100 mt-2"
          @click="exportInspections"
          :disabled="!selectedMonth || !selectedYear"
        >
          Descargar Registros
        </button>
      </div>
    </div>

    <!-- TARJETA PRINCIPAL -->
    <div class="card shadow rounded">
      <div class="card-body">
        <h4 class="card-title mb-4">REGISTRO DE INSPECCIÓN DE LOCKERS O CASILLEROS DE PERSONAL</h4>

        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label>Número de Locker</label>
            <input v-model="form.locker_number" class="form-control" required />
          </div>

          <div class="form-group">
            <label>Nombre</label>
            <input v-model="form.name" class="form-control" required />
          </div>

          <div v-for="field in itemFields" :key="field.key" class="form-group">
            <label>{{ field.label }}</label>
            <select v-model="form[field.key]" class="form-control" required>
              <option value="">Seleccione</option>
              <option value="CUMPLE">CUMPLE</option>
              <option value="NO CUMPLE">NO CUMPLE</option>
            </select>
          </div>

          <div class="form-group">
            <label>Observaciones</label>
            <textarea v-model="form.observations" class="form-control" rows="3"></textarea>
          </div>

          <!-- Firma -->
          <div class="form-group">
            <label>Firma</label>
            <div class="signature-container">
              <canvas ref="canvas"></canvas>
            </div>
            <button type="button" @click="clearSignature" class="btn btn-sm btn-secondary mt-2">
              Borrar Firma
            </button>
          </div>

          <button type="submit" class="btn btn-primary mt-3 w-100">Guardar Inspección</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import SignaturePad from 'signature_pad'
import axios from 'axios'

export default {
  setup() {
    const canvas = ref(null)
    let signaturePad = null

    const form = ref({
      locker_number: '',
      name: '',
      cleanliness: '',
      shoes: '',
      clothes: '',
      ppe: '',
      separate_uniform: '',
      no_medicine: '',
      no_food: '',
      no_tools: '',
      foreign_objects: '',
      observations: ''
    })

    const itemFields = [
      { key: 'cleanliness', label: 'Limpieza' },
      { key: 'shoes', label: 'Zapatos' },
      { key: 'clothes', label: 'Ropa' },
      { key: 'ppe', label: 'EPP' },
      { key: 'separate_uniform', label: 'Uniforme separado' },
      { key: 'no_medicine', label: 'No Medicamentos' },
      { key: 'no_food', label: 'No Alimentos' },
      { key: 'no_tools', label: 'No Herramientas' },
      { key: 'foreign_objects', label: 'Objetos Extraños' }
    ]

    const months = [
      'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]

    const years = [2024, 2025, 2026]
    const selectedMonth = ref('')
    const selectedYear = ref('')

    // Firma
    onMounted(() => {
      const ratio = window.devicePixelRatio || 1
      const canvasEl = canvas.value
      canvasEl.width = canvasEl.offsetWidth * ratio
      canvasEl.height = canvasEl.offsetHeight * ratio
      canvasEl.getContext('2d').scale(ratio, ratio)
      signaturePad = new SignaturePad(canvasEl, {
        penColor: 'black',
        backgroundColor: 'white'
      })
    })

    const clearSignature = () => {
      if (signaturePad) signaturePad.clear()
    }

    const submitForm = async () => {
      const signature = signaturePad?.isEmpty() ? null : signaturePad.toDataURL()
      const payload = { ...form.value, signature }

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/api/submit-locker-inspection`,
          payload
        )

        if (response.status === 201) {
          alert('Registro guardado exitosamente')
          Object.keys(form.value).forEach(k => form.value[k] = '')
          clearSignature()
        } else {
          alert('Error al guardar los datos')
        }
      } catch (error) {
        console.error("Error al enviar los datos:", error)
        alert('Error al conectar con el servidor')
      }
    }

    const exportInspections = async () => {
      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/api/export-locker-inspections`,
          {
            month: selectedMonth.value,
            year: selectedYear.value
          },
          { responseType: 'blob' }
        )

        const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `Inspeccion_Lockers_${selectedYear.value}_${String(selectedMonth.value).padStart(2, '0')}.xlsx`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
      } catch (error) {
        console.error("Error al exportar:", error)
        alert('No se pudieron obtener los registros del mes seleccionado.')
      }
    }

    return {
      form,
      itemFields,
      canvas,
      clearSignature,
      submitForm,
      months,
      years,
      selectedMonth,
      selectedYear,
      exportInspections
    }
  }
}
</script>

<style scoped>
.signature-container {
  border: 1px solid #ccc;
  height: 150px;
  background: white;
  position: relative;
}
canvas {
  width: 100%;
  height: 100%;
  touch-action: none;
}
</style>
