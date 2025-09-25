<template>
  <div class="container mt-5">

    <h2 class="text-center mb-4">Control de Faltas del Personal</h2>

    <div class="card shadow-sm">
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
        <div class="mb-4 w-50 mx-auto">
          <label for="personnelSearch" class="form-label">Buscar empleado:</label>
          <input type="text" v-model="personnelSearch" class="form-control" placeholder="Escribe para buscar..." />

          <select v-model="selectedPersonnel" class="form-select mt-2" @change="onPersonnelChange">
            <option disabled value="">Seleccionar...</option>
            <option v-for="person in filteredPersonnel" :key="person.id" :value="person">
              {{ person.name }}
            </option>
          </select>
        </div><br>

        <div v-if="selectedPersonnel" class="row mt-4">
          <!-- Columna A: Ahorcado -->
          <div class="col-md-4 text-center d-flex flex-column align-items-center">
            <h4>{{ selectedPersonnel.name }}</h4>

            <svg v-if="faultCount > 0" width="100%" height="300" viewBox="0 0 200 250">
              <!-- Poste y cuerda (1era falta) -->
              <line x1="25%" y1="80%" x2="25%" y2="8%" stroke="black" stroke-width="4" v-if="faultCount >= 1" />
              <line x1="25%" y1="8%" x2="60%" y2="8%" stroke="black" stroke-width="4" v-if="faultCount >= 1" />
              <line x1="60%" y1="8%" x2="60%" y2="16%" stroke="black" stroke-width="4" v-if="faultCount >= 1" />

              <!-- Cabeza (2da falta) -->
              <circle v-if="faultCount >= 2" cx="60%" cy="24%" r="8%" stroke="black" stroke-width="4" fill="none" />

              <!-- Ojos en forma de X cuando hay 5 faltas -->
              <g v-if="faultCount >= 5" stroke="red" stroke-width="2">
                <line x1="55%" y1="22%" x2="58%" y2="26%" />
                <line x1="58%" y1="22%" x2="55%" y2="26%" />
                <line x1="62%" y1="22%" x2="65%" y2="26%" />
                <line x1="65%" y1="22%" x2="62%" y2="26%" />
              </g>

              <!-- Cuerpo (3era falta) -->
              <line v-if="faultCount >= 3" x1="60%" y1="32%" x2="60%" y2="52%" stroke="black" stroke-width="4" />

              <!-- Brazos (4ta falta) -->
              <line v-if="faultCount >= 4" x1="60%" y1="40%" x2="45%" y2="36%" stroke="black" stroke-width="4" />
              <line v-if="faultCount >= 4" x1="60%" y1="40%" x2="75%" y2="36%" stroke="black" stroke-width="4" />

              <!-- Piernas (5ta falta) -->
              <line v-if="faultCount >= 5" x1="60%" y1="52%" x2="50%" y2="68%" stroke="black" stroke-width="4" />
              <line v-if="faultCount >= 5" x1="60%" y1="52%" x2="70%" y2="68%" stroke="black" stroke-width="4" />
            </svg>

            <p class="mt-2"><strong>{{ faultCountUnpenalized }} / 5 faltas acumuladas</strong></p>
          </div>


          <!-- Columna B: Formulario -->
          <div class="col-md-8">
            <div class="card p-3 shadow-sm mb-4">
              <h5 class="mb-3">Registrar nueva falta</h5>

              <div class="mb-3">
                <label class="form-label">Fecha del registro:</label>
                <input type="date" v-model="customDate" class="form-control" required>
              </div>

              <div class="mb-3">
                <label class="form-label">Responsable que aplica:</label>
                <input v-model="responsible" type="text" class="form-control text-uppercase" placeholder="Responsable"
                  required>
              </div>

              <div class="mb-3">
                <label class="form-label">Tipo de falta:</label>
                <select v-model="selectedFaultType" class="form-select">
                  <option disabled value="">Seleccionar tipo de falta...</option>
                  <option v-for="type in faultTypes" :key="type.id" :value="type.id">
                    {{ type.name }}
                  </option>
                </select>
              </div>

              <!-- Gravedad -->
              <div class="mb-3">
                <label class="form-label">Gravedad:</label>
                <select v-model="severity" class="form-select">
                  <option disabled value="">Seleccionar gravedad…</option>
                  <option value="LEVE">LEVE</option>
                  <option value="GRAVE">GRAVE</option>
                  <option value="MUY GRAVE">MUY GRAVE</option>
                </select>
              </div>

              <!-- ✅ Checkbox solo si es LEVE -->
              <div v-if="severity === 'LEVE'" class="form-check mb-3">
                <input v-model="levePenaltyCheck" type="checkbox" class="form-check-input" id="levePenaltyCheck">
                <label class="form-check-label" for="levePenaltyCheck">
                  Registrar multa
                </label>
              </div>

              <div class="mb-3">
                <label class="form-label">Descripción de la falta:</label>
                <textarea v-model="description" class="form-control text-uppercase" rows="3"
                  placeholder="Descripción de la falta"></textarea>
              </div>

              <!-- Multa: aparece si es GRAVE, MUY GRAVE o si el check de LEVE está marcado -->
              <div v-if="severity === 'GRAVE' || severity === 'MUY GRAVE' || levePenaltyCheck" class="mb-3">
                <label class="form-label">Valor de la multa:</label>
                <textarea v-model="penaltyDescription" class="form-control text-uppercase" rows="2"
                  placeholder="Descripción de la multa"></textarea>
              </div>

              <div v-if="severity === 'GRAVE' || severity === 'MUY GRAVE' || levePenaltyCheck" class="mb-3">
                <label class="form-label">N° Amonestación:</label>
                <input type="number" min="1" v-model="numeration" class="form-control" placeholder="N° Amonestación">
              </div>

              <button @click="addFault" class="btn btn-warning w-100 mt-2">Registrar</button>
            </div>
          </div>
        </div>

        <!-- Tabla de historial -->
        <div v-if="faults.length > 0" class="mt-4">
          <div class="card shadow-sm">
            <div class="card-header bg-danger text-white text-center">
              Historial de Faltas
            </div>
            <div class="card-body p-0" style="max-height: 300px; overflow-y: auto;">
              <table class="table table-bordered mb-0 table-hover">
                <thead class="table-light">
                  <tr>
                    <th style="width: 5%;"></th> <!-- columna para el icono -->
                    <th style="width: 20%;">Fecha</th>
                    <th>Descripción</th>
                    <th>Gravedad</th>
                    <th>Responsable</th>
                    <th>Tipo</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="fault in faults" :key="fault.id">
                    <!-- Fila normal -->
                    <tr :class="fault.penalized ? 'table-warning' : 'table-secondary'">
                      <!-- icono de expandir -->
                      <td class="text-center" @click="fault.penalty && toggleExpand(fault.id)" style="cursor: pointer;">
                        <span v-if="fault.penalty">
                          {{ expandedFaultId === fault.id ? '▼' : '▶' }}
                        </span>
                      </td>
                      <td>{{ fault.date }}</td>
                      <td>{{ fault.description }}</td>
                      <td>{{ fault.severity }}</td>
                      <td>{{ fault.responsible }}</td>
                      <td>{{ fault.type }}</td>
                    </tr>

                    <!-- Fila expandida si tiene multa -->
                    <tr v-if="expandedFaultId === fault.id && fault.penalty" class="table-light">
                      <td colspan="6">
                        <div class="p-2">
                          <strong>Multa asociada:</strong><br>
                          <ul class="mb-0">
                            <li><b>Descripción multa:</b> {{ fault.penalty.description }}</li>
                            <li><b>Numeración:</b> {{ fault.penalty.numeration || '—' }}</li>
                          </ul>
                        </div>
                      </td>
                    </tr>
                  </template>
                </tbody>

              </table>
            </div>
          </div>
        </div><br>

      </div>
    </div>
  </div><br>
</template>

<script>
export default {
  data() {
    return {
      personnelList: [],
      personnelSearch: '',
      selectedPersonnel: '',
      faultCount: 0,
      description: '',
      penaltyDescription: '',  // ← NUEVO para multa grave/muy grave
      faults: [],
      penaltyCreated: false,
      faultCountUnpenalized: 0,
      directPenaltyDescription: '',
      responsible: '',
      customDate: new Date().toISOString().split('T')[0], // valor por defecto: hoy
      faultTypes: [],
      selectedFaultType: '',
      severity: '',          //  para faltas
      numeration: null,       //  para multas
      levePenaltyCheck: false,   // ✅ Nuevo
      expandedFaultId: null
    };
  },
  computed: {
    // Filtra el personal según lo que escribas
    filteredPersonnel() {
      if (!this.personnelSearch) return this.personnelList;
      const search = this.personnelSearch.toLowerCase();
      return this.personnelList.filter(person =>
        person.name.toLowerCase().includes(search)
      );
    }
  },

  methods: {
    toggleExpand(faultId) {
      this.expandedFaultId = this.expandedFaultId === faultId ? null : faultId;
    },
    loadPersonnel() {
      fetch(`${process.env.VUE_APP_API_URL}/api/get-personnel-list`)
        .then(res => res.json())
        .then(data => {
          this.personnelList = data.personnel;
        })
        .catch(err => console.error('Error al cargar personal:', err));
    },
    loadFaultTypes() {
      fetch(`${process.env.VUE_APP_API_URL}/api/get-fault-types`)
        .then(res => res.json())
        .then(data => {
          this.faultTypes = data.types;
        })
        .catch(err => console.error('Error al cargar tipos de faltas:', err));
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
            // Normaliza la fecha y severity solo para mostrar
            this.faults = data.faults.map(fault => {
              const rawDate = typeof fault.date === 'string' ? fault.date : fault.date?.toString?.() || '';
              const date = new Date(rawDate + 'T00:00:00');
              const formattedDate = isNaN(date)
                ? 'N/A'
                : `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth() + 1).padStart(2, '0')}/${date.getFullYear()}`;

              return {
                ...fault,
                date: formattedDate,
                severity: (fault.severity || '').toString().trim().toUpperCase()
              };
            });

            // ✅ Usa lo que ya calculó el backend
            this.faultCount = data.active_faults;
            this.faultCountUnpenalized = data.active_faults;

            // (Opcional) Respaldo calculado en el front por si algo falla:
            // const levesNoPenalizadas = this.faults.filter(f => f.severity === 'LEVE' && !f.penalized);
            // this.faultCount = levesNoPenalizadas.length;
            // this.faultCountUnpenalized = levesNoPenalizadas.length;

            this.penaltyCreated = this.faultCountUnpenalized < 5;
          }
        })
        .catch(err => console.error('Error al obtener faltas:', err));

    },
    addFault() {
      if (!this.description.trim() || !this.selectedPersonnel || !this.responsible.trim() || !this.selectedFaultType) {
        alert("Completa todos los campos: descripción, empleado, responsable y tipo de falta.");
        return;
      }

      if ((this.severity === 'GRAVE' || this.severity === 'MUY GRAVE') && !this.penaltyDescription.trim()) {
        alert("Debes ingresar una descripción de la multa para faltas GRAVES o MUY GRAVES.");
        return;
      }

      const faultDescription = this.description.toUpperCase();
      const responsibleName = this.responsible.toUpperCase();
      const penaltyDesc = this.penaltyDescription?.toUpperCase() || null;
      const numeration = this.numeration;

      fetch(`${process.env.VUE_APP_API_URL}/api/faults`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          personnel_id: this.selectedPersonnel.id,
          description: faultDescription,
          responsible: responsibleName,
          date: this.customDate,
          fault_type_id: Number(this.selectedFaultType),  // ← forzar a entero
          severity: this.severity,
          numeration,
          penalty_description: penaltyDesc
        })
      })
        .then(async res => {
          if (!res.ok) {
            const errorText = await res.text();
            throw new Error(`Error HTTP ${res.status}: ${errorText}`);
          }
          return res.json();
        })
        .then(result => {
          if (this.severity === 'LEVE') {
            // Actualizar contador del ahorcado
            this.faultCountUnpenalized = result.active_faults;
            this.faultCount = result.active_faults;

            // Agregar la nueva falta leve al inicio de la tabla
            this.faults.unshift({
              id: result.fault_id,
              date: new Date(this.customDate + 'T00:00:00').toLocaleDateString('es-EC'),
              description: faultDescription,
              severity: 'LEVE',
              responsible: responsibleName,
              type: this.faultTypes.find(t => t.id === Number(this.selectedFaultType))?.name || '',
              type_color: 'falta'  // table-secondary
            });
          } else {
            // Para faltas GRAVES/MUY GRAVES recarga todo
            this.fetchFaults();
          }

          if (this.faultCountUnpenalized >= 5) {
            this.penaltyCreated = false;
          }

          // Limpiar formulario
          this.description = '';
          this.responsible = '';
          this.penaltyDescription = '';
          this.numeration = null;
          this.levePenaltyCheck = false;
        })

        .catch(err => {
          console.error('Error al registrar la falta:', err);
          alert(`Error al registrar la falta:\n${err.message}`);
        });
    },
    goHome() {
      this.$router.push('/home-penalties'); // Asegúrate de que la ruta '/' sea tu página de inicio
    }

  },
  mounted() {
    this.loadPersonnel();
    this.loadFaultTypes();
  },

};
</script>

<style scoped>
.header-custom {
  background: linear-gradient(90deg, #dc3545, #ff6f61);
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 0.375rem 0.375rem 0 0;
}

.card-body {
  padding: 20px;
}

.form-label {
  font-weight: 500;
}

.card p,
.card h4,
.card h5 {
  margin-bottom: 15px;
}

.table-hover tbody tr:hover {
  background-color: #ffeaea;
}
</style>