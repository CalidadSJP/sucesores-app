<template>
  <div class="container mt-4">
    <div class="card shadow rounded">

      <!-- HEADER de la Tarjeta -->
      <div class="card-header bg-primary text-white d-flex align-items-center justify-content-between flex-wrap"
        style="min-height: 80px;">
        <!-- Icono y Título -->
        <div class="d-flex align-items-center">
          <h2 class="mb-0 fs-3">Revisión de Sondas</h2>
        </div>

        <!-- Botones -->
        <div class="d-flex gap-2 mt-3 mt-md-0">
          <button class="btn btn-outline-light px-4 py-2 fs-5" @click="$router.push('/pieces-record')">
            <i class="fas fa-clipboard-list me-1"></i> Registro
          </button>
          <button class="btn btn-outline-light px-4 py-2 fs-5" @click="$router.push('/')">
            <i class="fas fa-arrow-left me-1"></i> Regresar
          </button>
        </div>
      </div>




      <div class="card-body">
        <form @submit.prevent="submitForm">
          <!-- Línea de Producción -->
          <div class="mb-3">
            <label class="form-label">
              <i class="fas fa-industry me-2"></i>Línea de Producción
            </label>
            <select v-model="selectedLine" @change="onLineChange" class="form-select" required>
              <option disabled value="">Seleccione Línea</option>
              <option v-for="line in productionLines" :key="line.id" :value="line.id">
                {{ line.line_name }}
              </option>
            </select>
          </div>

          <!-- Piezas de la Línea -->
          <div class="mb-3" v-if="filteredPieces.length">
            <label class="form-label">
              <i class="fas fa-cogs me-2"></i>Elemento
            </label>
            <select v-model="form.piece" class="form-select" required>
              <option disabled value="">Seleccione Elemento</option>
              <option v-for="piece in filteredPieces" :key="piece" :value="piece">
                {{ piece }}
              </option>
            </select>
          </div>

          <!-- Fecha de Inspección -->
          <div class="mb-4">
            <label class="form-label">
              <i class="fas fa-calendar-alt me-2"></i>Fecha de Inspección
            </label>
            <input type="date" v-model="form.inspection_date" class="form-control" required />
          </div>

          <!-- Campos de Evaluación Agrupados -->
          <div v-for="section in evaluationSections" :key="section.title" class="mb-4 p-3 border rounded bg-light">
            <h5 class="mb-3">
              <i class="fas fa-clipboard-check me-2 text-primary"></i>{{ section.title }}
            </h5>

            <div class="row g-3">
              <div class="col-md-4" v-for="field in section.fields" :key="field.key">
                <label class="form-label">{{ field.label }}</label>
                <select v-model="form[field.key]" class="form-select" required>
                  <option value="">Seleccione</option>
                  <option value="BIEN">BIEN</option>
                  <option value="MAL">MAL</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Observaciones -->
          <div class="mb-4">
            <label class="form-label">
              <i class="fas fa-comment-alt me-2"></i>Observaciones
            </label>
            <textarea v-model="form.observations" class="form-control" rows="3"
              placeholder="Escriba observaciones..."></textarea>
          </div>

          <button type="submit" class="btn btn-success w-100">
            <i class="fas fa-save me-2"></i>Guardar Inspección
          </button>
        </form>
      </div>
    </div>
  </div><br><br>
</template>


<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const productionLines = ref([])
    const selectedLine = ref('')

    const linePieces = {
      'TALLARINES': [
        'Rotronic Cuarto 1', 'Rotronic Cuarto 2', 'Rotronic Cuarto 3',
        'Rotronic Cuarto 4', 'Rotronic Cuarto 5'
      ],
      'FAVA PASTA LARGA': [
        'Rotronic Presecador Z1(RFPL-Z1)', 'Rotronic Presecador Z2(RFPL-Z2)', 'Rotronic Presecador Z3(RFPL-Z3)',
        'Rotronic GPL1', 'Rotronic GLP2(RFPL-ENF)', 'Rotronic GPL2 (RFPL-ENF)', 'Rotronic Humidificador'
      ],
      'PAVAN': [
        'Rotronic Central 1', 'Rotronic Central 2-3', 'Rotronic Central 4-5',
        'Rotronic Central 6-7', 'Rotronic Central 8-9', 'Rotronic Piso 1', 'Rotronic Piso 2', 'Rotronic Piso 3'
      ],
      'B600': ['Rotronic Secador (RB6-TS)', 'Medidor de temperatura'],
      'FAVA PASTA CORTA': ['Medidor de temperatura Trabato', 'Rotronic Presecador', 'Rotronic Secador'],
      'B1000': [
        'Rotronic Trabato Z1', 'Rotronic Secador Z2', 'Rotronic Secador Z3',
        'Rotronic Secador Z4', 'Rotronic Secador Z5'
      ],
      'FAVA 2200': ['Medidor de Temperatura Trabato', 'Rotronic Presecador', 'Rotronic Secador']
    }

    const form = ref({
      piece: '',
      inspection_date: '',
      mesh: '',
      screw: '',
      bulb_plastic: '',
      connector_mounting: '',
      connector_adjustment: '',
      connector_plastic: '',
      transducer_adjustment: '',
      probe_plastic: '',
      observations: ''
    })

    const evaluationSections = [
      {
        title: 'REVISION DE BULBO',
        fields: [
          { key: 'mesh', label: 'Malla' },
          { key: 'screw', label: 'Tornillo' },
          { key: 'bulb_plastic', label: 'Plástico' }
        ]
      },
      {
        title: 'REVISION DEL CONECTOR DE ALIMENTACION',
        fields: [
          { key: 'connector_mounting', label: 'Sujeción' },
          { key: 'connector_adjustment', label: 'Ajuste (Tuerca)' },
          { key: 'connector_plastic', label: 'Plástico' }
        ]
      },
      {
        title: 'REVISION DEL CONECTOR SONDA',
        fields: [
          { key: 'transducer_adjustment', label: 'Ajuste al transductor' },
          { key: 'probe_plastic', label: 'Plástico' }
        ]
      }
    ]

    const filteredPieces = computed(() => {
      const line = productionLines.value.find(l => l.id === selectedLine.value)
      return line ? linePieces[line.line_name] || [] : []
    })

    const onLineChange = () => {
      form.value.piece = ''
    }

    const fetchProductionLines = async () => {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-lines`)
        productionLines.value = response.data
      } catch (error) {
        console.error('Error fetching production lines:', error)
      }
    }

    const submitForm = async () => {
      try {
        const payload = { ...form.value, line_id: selectedLine.value }
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/submit-piece-inspection`, payload)

        if (response.status === 201) {
          alert('Inspección guardada exitosamente')
          Object.keys(form.value).forEach(k => form.value[k] = '')
          selectedLine.value = ''
        } else {
          alert('Error al guardar los datos')
        }
      } catch (error) {
        console.error('Error al enviar los datos:', error)
        alert('Error al conectar con el servidor')
      }
    }

    onMounted(() => {
      fetchProductionLines()
    })

    return {
      productionLines,
      selectedLine,
      form,
      evaluationSections,
      filteredPieces,
      onLineChange,
      submitForm
    }

  }
}
</script>

<style scoped></style>
