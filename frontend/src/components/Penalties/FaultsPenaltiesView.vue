<template>
  <div class="page-wrapper">

    <div class="big-card shadow-lg rounded">

      <!-- Header dentro de la tarjeta -->
      <div class="header-box p-3 text-white d-flex justify-content-between align-items-center">

        <div class="d-flex align-items-center">
          <i class="fas fa-user-times fa-2x me-3"></i>
          <div>
            <h2 class="mb-0">Control de Faltas y Multas</h2>
            <small class="fw-light">Registro y seguimiento de personal</small>
          </div>
        </div>

        <!-- CONTENEDOR DE BOTONES DEL HEADER -->
        <div class="header-buttons d-flex align-items-center">

          <!-- Grupo: Faltas + Multas -->
          <div class="tab-group d-flex gap-2">
            <button @click="selectTab('faults')" :class="['tab-btn', activeTab === 'faults' ? 'active' : '']">
              <i class="fas fa-user-times me-1"></i> Faltas
            </button>

            <button @click="selectTab('penalties')" :class="['tab-btn', activeTab === 'penalties' ? 'active' : '']">
              <i class="fas fa-gavel me-1"></i> Multas
            </button>
          </div>

          <!-- Botón Regresar alineado a la derecha -->
          <button @click="$router.back()" class="btn btn-light text-success fw-bold ms-auto">
            <i class="fas fa-arrow-left me-2"></i> Regresar
          </button>

        </div>


      </div>



      <div class="card-body">


        <div class="tab-content" id="faultPenaltyTabsContent">
          <!-- ============================
      TAB FALTAS
============================= -->
          <div v-if="activeTab === 'faults'">
            <div class="table-responsive">
              <table class="table table-bordered table-striped">
                <thead class="table-dark">
                  <tr>
                    <th>Fecha</th>
                    <th>Empleado</th>
                    <th>Descripción</th>
                    <th>Responsable</th>
                    <th>Tipo</th>
                    <th>Gravedad</th>
                  </tr>

                  <!-- fila de filtros FALTAS -->
                  <tr class="bg-light">
                    <th><input v-model="filtersFaults.date" class="form-control form-control-sm"></th>
                    <th><input v-model="filtersFaults.employee" class="form-control form-control-sm"></th>
                    <th><input v-model="filtersFaults.description" class="form-control form-control-sm"></th>
                    <th><input v-model="filtersFaults.responsible" class="form-control form-control-sm"></th>
                    <th><input v-model="filtersFaults.type" class="form-control form-control-sm"></th>
                    <th>
                      <select v-model="filtersFaults.severity" class="form-select form-select-sm">
                        <option value=""></option>
                        <option value="LEVE">LEVE</option>
                        <option value="GRAVE">GRAVE</option>
                        <option value="MUY GRAVE">MUY GRAVE</option>
                      </select>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="fault in paginatedFaults" :key="fault.id">
                    <td>{{ fault.date }}</td>
                    <td>{{ fault.full_name }}</td>
                    <td>{{ fault.description }}</td>
                    <td>{{ fault.responsible }}</td>
                    <td>{{ fault.type }}</td>
                    <td>{{ fault.severity }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- PAGINACIÓN FALTAS -->
            <div class="pagination-container">
              <button @click="prevPage('faults')" :disabled="faultPage === 1">Anterior</button>
              <button @click="jumpPages('faults', -10)" :disabled="faultPage <= 10">«</button>
              <button v-for="page in faultPageNumbers" :key="'f' + page" @click="faultPage = page"
                :class="{ active: faultPage === page }">
                {{ page }}
              </button>
              <button @click="jumpPages('faults', 10)" :disabled="faultPage + 10 > totalFaultPages">»</button>
              <button @click="nextPage('faults')" :disabled="faultPage === totalFaultPages">Siguiente</button>
            </div>
          </div>


          <!-- ============================
      TAB MULTAS
============================= -->
          <div v-if="activeTab === 'penalties'">
            <div class="table-responsive">
              <table class="table table-bordered table-striped">
                <thead class="table-dark">
                  <tr>
                    <th>Fecha</th>
                    <th>Empleado</th>
                    <th>Descripción de la falta</th>
                    <th>Descripción de la multa</th>
                    <th>Responsable</th>
                    <th>Tipo</th>
                    <th>N° Amonestación</th>
                  </tr>

                  <!-- fila de filtros MULTAS -->
                  <tr class="bg-light">
                    <th><input v-model="filtersPenalties.date" class="form-control form-control-sm"></th>
                    <th><input v-model="filtersPenalties.employee" class="form-control form-control-sm"></th>
                    <th><input v-model="filtersPenalties.fault_description" class="form-control form-control-sm"></th>
                    <th><input v-model="filtersPenalties.description" class="form-control form-control-sm"></th>
                    <th><input v-model="filtersPenalties.responsible" class="form-control form-control-sm"></th>
                    <th><input v-model="filtersPenalties.type" class="form-control form-control-sm"></th>
                    <th><input v-model="filtersPenalties.numeration" class="form-control form-control-sm" type="number"
                        min="1"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="penalty in paginatedPenalties" :key="penalty.id">
                    <td>{{ penalty.date }}</td>
                    <td>{{ penalty.full_name }}</td>
                    <td class="text-truncate fault-desc" :title="penalty.fault_description">
                      {{ penalty.fault_description }}
                    </td>
                    <td>{{ penalty.description }}</td>
                    <td>{{ penalty.responsible }}</td>
                    <td>{{ penalty.type }}</td>
                    <td>{{ penalty.numeration }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- PAGINACIÓN MULTAS -->
            <div class="pagination-container">
              <button @click="prevPage('penalties')" :disabled="penaltyPage === 1">Anterior</button>
              <button @click="jumpPages('penalties', -10)" :disabled="penaltyPage <= 10">«</button>
              <button v-for="page in penaltyPageNumbers" :key="'p' + page" @click="penaltyPage = page"
                :class="{ active: penaltyPage === page }">
                {{ page }}
              </button>
              <button @click="jumpPages('penalties', 10)" :disabled="penaltyPage + 10 > totalPenaltyPages">»</button>
              <button @click="nextPage('penalties')" :disabled="penaltyPage === totalPenaltyPages">Siguiente</button>
            </div>
          </div>

        </div>

      </div>
    </div>
    <!-- Fin Card -->

  </div><br><br>
</template>


<script>
import axios from 'axios';

export default {
  name: 'FaultsPenaltiesView',
  data() {

    return {
      activeTab: 'faults',
      faults: [],
      penalties: [],
      filtersFaults: {
        date: '', employee: '', description: '',
        responsible: '', type: '', severity: '',
      },
      filtersPenalties: {
        date: '', employee: '', description: '',
        responsible: '', type: '', numeration: '', fault_description: ''
      },
      faultPage: 1,
      penaltyPage: 1,
      perPage: 10
    };

  },
  computed: {

    faultPageNumbers() {
      const groupSize = 5;
      const start = Math.floor((this.faultPage - 1) / groupSize) * groupSize + 1;
      return Array.from({ length: Math.min(groupSize, this.totalFaultPages - start + 1) }, (_, i) => start + i);
    },
    penaltyPageNumbers() {
      const groupSize = 5;
      const start = Math.floor((this.penaltyPage - 1) / groupSize) * groupSize + 1;
      return Array.from({ length: Math.min(groupSize, this.totalPenaltyPages - start + 1) }, (_, i) => start + i);
    },
    /* --- FILTRO y PAGINACIÓN FALTAS --- */
    filteredFaults() {
      const f = this.filtersFaults;
      return this.faults.filter(r =>
        String(r.date).toLowerCase().includes(f.date.toLowerCase()) &&
        String(r.full_name).toLowerCase().includes(f.employee.toLowerCase()) &&
        String(r.description).toLowerCase().includes(f.description.toLowerCase()) &&
        String(r.responsible).toLowerCase().includes(f.responsible.toLowerCase()) &&
        String(r.type).toLowerCase().includes(f.type.toLowerCase()) &&
        (f.severity ? String(r.severity).toLowerCase() === f.severity.toLowerCase() : true)
      );
    },

    filteredPenalties() {
      const f = this.filtersPenalties;
      return this.penalties.filter(r =>
        String(r.date).toLowerCase().includes(f.date.toLowerCase()) &&
        String(r.full_name).toLowerCase().includes(f.employee.toLowerCase()) &&
        String(r.fault_description).toLowerCase().includes(f.fault_description.toLowerCase()) &&
        String(r.description).toLowerCase().includes(f.description.toLowerCase()) &&
        String(r.responsible).toLowerCase().includes(f.responsible.toLowerCase()) &&
        String(r.type).toLowerCase().includes(f.type.toLowerCase()) &&
        (f.numeration ? String(r.numeration).includes(f.numeration) : true)
      );
    },
    totalFaultPages() { return Math.ceil(this.filteredFaults.length / this.perPage); },
    paginatedFaults() {
      const start = (this.faultPage - 1) * this.perPage;
      return this.filteredFaults.slice(start, start + this.perPage);
    },

    /* --- FILTRO y PAGINACIÓN MULTAS --- */
    totalPenaltyPages() { return Math.ceil(this.filteredPenalties.length / this.perPage); },
    paginatedPenalties() {
      const start = (this.penaltyPage - 1) * this.perPage;
      return this.filteredPenalties.slice(start, start + this.perPage);
    },


  },
  mounted() {
    this.fetchFaults();
    this.fetchPenalties();
  },
  methods: {

    selectTab(tab) {
      this.activeTab = tab;
    },

    downloadPenaltyPDF(id) {
      const url = `${process.env.VUE_APP_API_URL}/api/generate-penalty-pdf/${id}`;
      window.open(url, "_blank");
    },

    formatDate(dateStr) {
      if (!dateStr || typeof dateStr !== 'string') return 'N/A';

      const [year, month, day] = dateStr.split('T')[0].split('-'); // Extrae solo la parte de la fecha
      if (!year || !month || !day) return 'Fecha inválida';

      return `${day.padStart(2, '0')}/${month.padStart(2, '0')}/${year}`;
    }
    ,
    fetchFaults() {
      axios.get(`${process.env.VUE_APP_API_URL}/api/get-faults`)
        .then(response => {
          if (Array.isArray(response.data)) {
            this.faults = response.data.map(fault => ({
              ...fault,
              date: this.formatDate(fault.date)
            }));
          } else {
            console.error('Formato inesperado en /get-faults:', response.data);
          }
        })
        .catch(error => {
          console.error('Error al obtener faltas:', error);
        });
    },
    fetchPenalties() {
      axios.get(`${process.env.VUE_APP_API_URL}/api/get-penalties`)
        .then(response => {
          if (Array.isArray(response.data)) {
            this.penalties = response.data.map(penalty => ({
              ...penalty,
              date: this.formatDate(penalty.date)
            }));
          } else {
            console.error('Formato inesperado en /get-penalties:', response.data);
          }
        })
        .catch(error => {
          console.error('Error al obtener multas:', error);
        });
    },
    nextPage(type) {
      if (type === 'faults' && this.faultPage < this.totalFaultPages) this.faultPage++;
      if (type === 'penalties' && this.penaltyPage < this.totalPenaltyPages) this.penaltyPage++;
    },
    prevPage(type) {
      if (type === 'faults' && this.faultPage > 1) this.faultPage--;
      if (type === 'penalties' && this.penaltyPage > 1) this.penaltyPage--;
    },
    jumpPages(type, count) {
      if (type === 'faults') {
        const newPage = Math.min(Math.max(1, this.faultPage + count), this.totalFaultPages);
        this.faultPage = newPage;
      }
      if (type === 'penalties') {
        const newPage = Math.min(Math.max(1, this.penaltyPage + count), this.totalPenaltyPages);
        this.penaltyPage = newPage;
      }
    }
  }
};
</script>

<style scoped>
/* ===========================
   TABLAS
=========================== */
.table th,
.table td {
  vertical-align: middle;
  white-space: nowrap;
}

.table-responsive {
  overflow-x: auto;
}

/* ===========================
   PAGINACIÓN
=========================== */
.pagination-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 1rem;
}

.pagination-container button {
  background-color: #28a745;
  border: none;
  color: white;
  padding: 8px 14px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.pagination-container button.active {
  background-color: #1e7e34;
}

.pagination-container button:hover:not(:disabled) {
  background-color: #218838;
}

.pagination-container button:disabled {
  background-color: #c3e6cb;
  cursor: not-allowed;
}

.pagination-container button:not(:first-child):not(:last-child) {
  border-radius: 50%;
}

/* ===========================
   TARJETA PRINCIPAL
=========================== */
.page-wrapper {
  width: 100%;
  padding: 20px;
  padding-bottom: 40px;
  box-sizing: border-box;
}

.big-card {
  width: 100%;
  max-width: 100%;
  background: white;
  margin: 0 auto;
  border-radius: 18px;
  overflow: hidden;
}

.card-body {
  width: 100%;
  padding: 25px !important;
  padding-top: 30px !important;
  box-sizing: border-box;
}

/* ===========================
   HEADER DE LA TARJETA
=========================== */
.header-box {
  width: 100%;
  background: linear-gradient(135deg, #28a745, #218838);
  border-left: 5px solid #1e7e34;
  border-radius: 18px 18px 0 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

/* ===========================
   BOTONES DE PESTAÑAS
=========================== */
.tab-btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: 2px solid #ffffff55;
  background: #ffffff22;
  color: white;
  font-weight: bold;
  transition: 0.25s;
}

.tab-btn:hover {
  background: #ffffff33;
  border-color: #fff;
}

.tab-btn.active {
  background: white !important;
  color: #218838 !important;
  border-color: white !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

/* ===========================
   CONTENEDOR BOTONES HEADER
=========================== */
.header-buttons {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 20px;
}

.tab-group {
  display: flex;
  gap: 6px;
}

.header-buttons .btn {
  margin-left: auto;
}

/* ===========================
   DESCRIPCIÓN TRUNCADA
=========================== */
.fault-desc {
  max-width: 180px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ===========================
   RESPONSIVE
=========================== */
@media (max-width: 992px) {
  .header-box h2 {
    font-size: 1.4rem;
  }

  .header-box small {
    font-size: 0.85rem;
  }
}

@media (max-width: 768px) {
  .header-box {
    text-align: center;
  }

  .header-buttons {
    flex-direction: column;
    gap: 10px;
  }

  .header-buttons .btn {
    width: 100%;
    margin-left: 0 !important;
  }

  .tab-group {
    width: 100%;
    justify-content: center;
  }

  table input.form-control-sm,
  table select.form-select-sm {
    min-width: 70px;
    font-size: 0.75rem;
  }
}

@media (max-width: 576px) {
  .header-box h2 {
    font-size: 1.1rem;
  }

  .card-body {
    padding: 0.4rem !important;
  }

  table {
    font-size: 0.75rem;
  }

  .pagination-container button {
    padding: 6px 10px;
    font-size: 0.75rem;
  }
}

/* Empuja los botones un poco hacia abajo */
.header-buttons {
  margin-left: 50px;
}

</style>
