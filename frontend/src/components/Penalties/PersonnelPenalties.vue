<template>
  <div class="container mt-5">

    <h2 class="text-center mb-4">Control de Faltas del Personal</h2>
    <div class="card">
      <div class="card-header text-white d-flex justify-content-between align-items-center header-custom">
        <div class="d-flex align-items-center">
          <i class="fas fa-user-check me-2"></i> Panel de Control
        </div>
        <button class="btn btn-outline-light btn-lg" @click="goHome">
          <i class="fas fa-arrow-left me-1"></i> Regresar
        </button>
      </div>


      <div class="card-body">
        <!-- Selector de empleado -->
        <div class="mb-4 w-100 mx-auto">
          <label for="personnelSelect" class="form-label">Seleccionar empleado:</label>
          <select v-model="selectedPersonnel" class="form-select" @change="onPersonnelChange">
            <option disabled value="">Seleccionar...</option>
            <option v-for="person in personnelList" :key="person.id" :value="person">
              {{ person.name }}
            </option>
          </select>
        </div>

        <div v-if="selectedPersonnel" class="text-center mt-4">
          <h4>{{ selectedPersonnel.name }}</h4>

          <svg v-if="faultCount > 0" width="200" height="250">
            <!-- Poste y cuerda (1era falta) -->
            <line x1="50" y1="200" x2="50" y2="20" stroke="black" stroke-width="4" v-if="faultCount >= 1" />
            <line x1="50" y1="20" x2="120" y2="20" stroke="black" stroke-width="4" v-if="faultCount >= 1" />
            <line x1="120" y1="20" x2="120" y2="40" stroke="black" stroke-width="4" v-if="faultCount >= 1" />

            <!-- Cabeza (2da falta) -->
            <circle v-if="faultCount >= 2" cx="120" cy="60" r="20" stroke="black" stroke-width="4" fill="none" />

            <!-- Ojos en forma de X cuando hay 5 faltas -->
            <g v-if="faultCount >= 5" stroke="red" stroke-width="2">
              <!-- Ojo izquierdo (X) -->
              <line x1="110" y1="55" x2="115" y2="60" />
              <line x1="115" y1="55" x2="110" y2="60" />

              <!-- Ojo derecho (X) -->
              <line x1="125" y1="55" x2="130" y2="60" />
              <line x1="130" y1="55" x2="125" y2="60" />
            </g>


            <!-- Cuerpo (3era falta) -->
            <line v-if="faultCount >= 3" x1="120" y1="80" x2="120" y2="130" stroke="black" stroke-width="4" />

            <!-- Brazos (4ta falta) -->
            <line v-if="faultCount >= 4" x1="120" y1="100" x2="90" y2="90" stroke="black" stroke-width="4" />
            <line v-if="faultCount >= 4" x1="120" y1="100" x2="150" y2="90" stroke="black" stroke-width="4" />

            <!-- Piernas (5ta falta) -->
            <line v-if="faultCount >= 5" x1="120" y1="130" x2="100" y2="170" stroke="black" stroke-width="4" />
            <line v-if="faultCount >= 5" x1="120" y1="130" x2="140" y2="170" stroke="black" stroke-width="4" />
          </svg>

          <p class="mt-2"><strong>{{ faultCountUnpenalized }} / 5 faltas acumuladas</strong></p>

          <!-- Botón para generar multa (basado en faltas activas no penalizadas) -->
          <button v-if="faultCountUnpenalized >= 5 && !penaltyCreated" @click="generatePenalty"
            class="btn btn-warning mb-3">
            Generar Multa
          </button>


          <!-- Formulario de falta -->
          <div class="input-group mb-3 w-100 mx-auto">
            <input v-model="description" type="text" class="form-control text-uppercase"
              placeholder="Descripción de la falta">
            <button @click="addFault" class="btn btn-danger">Registrar Falta</button>
          </div>

          <!-- Generar multa directamente sin contar faltas -->
          <div class="input-group mb-3 w-100 mx-auto">
            <input v-model="directPenaltyDescription" type="text" class="form-control text-uppercase"
              placeholder="Descripción de la multa directa">
            <button @click="addDirectPenalty" class="btn btn-success">Registrar Multa</button>
          </div>

          <div class="mb-3 w-100 mx-auto">
            <label for="responsibleSelect" class="form-label">Responsable que aplica:</label>
            <input v-model="responsible" type="text" class="form-control text-uppercase" required>
          </div>


          <!-- Tabla de faltas dentro de una tarjeta scrolleable -->
          <div v-if="faults.length > 0" class="mt-4 w-100 mx-auto">
            <div class="card shadow-sm">
              <div class="card-header bg-danger text-white text-center">
                Historial de Faltas
              </div>
              <div class="card-body p-0" style="max-height: 300px; overflow-y: auto;">
                <table class="table table-bordered mb-0">
                  <thead class="table-light">
                    <tr>
                      <th style="width: 20%;">Fecha</th>
                      <th>Descripción</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="fault in faults" :key="fault.id">
                      <td>{{ fault.date }}</td>
                      <td>{{ fault.description }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div><br><br>
</template>

<script>
export default {
  data() {
    return {
      personnelList: [],
      selectedPersonnel: '',
      faultCount: 0,
      description: '',
      faults: [],
      penaltyCreated: false,
      faultCountUnpenalized: 0,
      directPenaltyDescription: '',
      responsible: ''

    };
  },
  methods: {
    loadPersonnel() {
      fetch(`${process.env.VUE_APP_API_URL}/api/get-personnel-list`)
        .then(res => res.json())
        .then(data => {
          this.personnelList = data.personnel;
        })
        .catch(err => console.error('Error al cargar personal:', err));
    },
    onPersonnelChange() {
      this.description = '';
      this.faultCount = 0;
      this.faults = [];
      this.fetchFaults();
      this.penaltyCreated = false;

    },
    fetchFaults() {
      if (!this.selectedPersonnel) return;
      fetch(`${process.env.VUE_APP_API_URL}/api/faults/${this.selectedPersonnel.id}`)
        .then(res => res.json())
        .then(data => {
          if (data && Array.isArray(data.faults)) {
            // Formatear fechas antes de asignar
            this.faults = data.faults.map(fault => {
              const date = new Date(fault.date);
              const formattedDate = `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth() + 1).padStart(2, '0')}/${date.getFullYear()}`;
              return { ...fault, date: formattedDate };
            });

            this.faultCount = data.active_faults;
            this.faultCountUnpenalized = data.active_faults;
            this.penaltyCreated = this.faultCountUnpenalized < 5;
          }
        })
        .catch(err => console.error('Error al obtener faltas:', err));
    },
    addFault() {
      if (!this.description.trim() || !this.selectedPersonnel || !this.responsible.trim()) {
        alert("Completa la descripción, selecciona un empleado y especifica el responsable.");
        return;
      }

      const faultDescription = this.description.toUpperCase();
      this.description = '';

      const responsibleName = this.responsible.toUpperCase();
      this.responsible = '';

      this.$nextTick(() => {
        setTimeout(() => {
          fetch(`${process.env.VUE_APP_API_URL}/api/faults`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              personnel_id: this.selectedPersonnel.id,
              description: faultDescription,
              responsible: responsibleName
            })
          })
            .then(res => res.json())
            .then((result) => {
              this.faultCountUnpenalized = result.active_faults;
              this.fetchFaults();
              if (this.faultCountUnpenalized >= 5) {
                this.penaltyCreated = false;
              }
            })
            .catch(err => console.error('Error al registrar la falta:', err));
        }, 500);
      });
    },
    generatePenalty() {
      fetch(`${process.env.VUE_APP_API_URL}/api/generate-penalty`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ personnel_id: this.selectedPersonnel.id })
      })
        .then(res => res.json())
        .then(result => {
          if (result.status === 'success') {
            // Vaciar la lista de faltas
            this.faults = [];  // Vaciamos la tabla de faltas

            // Actualizar el contador de faltas no penalizadas
            this.faultCountUnpenalized = result.active_faults; // Este valor debería ser correcto después de la multa

            // Recargar las faltas no penalizadas
            this.fetchFaults(); // Recargar las faltas no penalizadas

            this.penaltyCreated = true;
            alert('✅ Multa generada exitosamente.');
          } else {
            alert('⚠️ No se pudo generar la multa.');
          }
        })
        .catch(err => console.error('Error al generar multa:', err));
    },
    addDirectPenalty() {
      if (!this.directPenaltyDescription.trim() || !this.selectedPersonnel || !this.responsible.trim()) {
        alert("Completa la descripción, selecciona un empleado y especifica el responsable.");
        return;
      }

      const penaltyDescription = this.directPenaltyDescription.toUpperCase();
      this.directPenaltyDescription = '';

      const responsibleName = this.responsible.toUpperCase();
      this.responsible = '';

      fetch(`${process.env.VUE_APP_API_URL}/api/generate-direct-penalty`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          personnel_id: this.selectedPersonnel.id,
          description: penaltyDescription,
          responsible: responsibleName
        })
      })
        .then(res => res.json())
        .then(result => {
          if (result.status === 'success') {
            alert('✅ Multa directa registrada exitosamente.');
            this.fetchFaults();
          } else {
            alert('⚠️ No se pudo registrar la multa directa.');
          }
        })
        .catch(err => console.error('Error al registrar multa directa:', err));
    },
    goHome() {
      this.$router.push('/home-penalties'); // Asegúrate de que la ruta '/' sea tu página de inicio
    }



  },
  mounted() {
    this.loadPersonnel();
  }
};
</script>

<style scoped>
svg {
  margin-bottom: 20px;
}

.card-body {
  padding: 20px;
}

.header-custom {
  background: linear-gradient(90deg, #dc3545, #ff6f61);
  /* Degradado rojo a naranja */
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 0.375rem 0.375rem 0 0;
}
</style>