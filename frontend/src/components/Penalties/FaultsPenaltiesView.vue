<template>
  <div class="container mt-4">
    <div class="header-box d-flex justify-content-between align-items-center p-3 mb-4  rounded bg-success text-white">
      <div class="d-flex align-items-center">
        <i class="fas fa-user-times fa-2x me-3"></i>
        <div>
          <h2 class="mb-0">Control de Faltas y Multas</h2>
          <small class="fw-light">Registro y seguimiento de personal</small>
        </div>
      </div>
      <button @click="$router.back()" class="btn btn-light text-success fw-bold" style="opacity: 1; transition: none;">
        <i class="fas fa-arrow-left me-2"></i> Regresar
      </button>

    </div>


    <!-- Card -->
    <div class="card shadow">
      <div class="card-body">

        <!-- Pestañas -->
        <ul class="nav nav-tabs mb-4" id="faultPenaltyTabs" role="tablist">
          <li class="nav-item" role="presentation">
            <button class="nav-link active" id="faults-tab" data-bs-toggle="tab" data-bs-target="#faults" type="button"
              role="tab">
              <i class="fas fa-user-times me-1"></i> Faltas
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" id="penalties-tab" data-bs-toggle="tab" data-bs-target="#penalties" type="button"
              role="tab">
              <i class="fas fa-gavel me-1"></i> Multas
            </button>
          </li>
        </ul>

        <div class="tab-content" id="faultPenaltyTabsContent">
          <!-- TAB: Faltas -->
          <div class="tab-pane fade show active" id="faults" role="tabpanel">
            <div class="table-responsive">
              <table class="table table-bordered table-striped">
                <thead class="table-dark">
                  <tr>
                    <th>Fecha</th>
                    <th>Empleado</th>
                    <th>Descripción</th>
                    <th>Responsable</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="fault in paginatedFaults" :key="fault.id">
                    <td>{{ fault.date }}</td>
                    <td>{{ fault.full_name }}</td>
                    <td>{{ fault.description }}</td>
                    <td>{{ fault.responsible }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
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

          <!-- TAB: Multas -->
          <div class="tab-pane fade" id="penalties" role="tabpanel">
            <div class="table-responsive">
              <table class="table table-bordered table-striped">
                <thead class="table-dark">
                  <tr>
                    <th>Fecha</th>
                    <th>Empleado</th>
                    <th>Descripción</th>
                    <th>Responsable</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="penalty in paginatedPenalties" :key="penalty.id">
                    <td>{{ penalty.date }}</td>
                    <td>{{ penalty.full_name }}</td>
                    <td>{{ penalty.description }}</td>
                    <td>{{ penalty.responsible }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
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
      faults: [],
      penalties: [],
      faultPage: 1,
      penaltyPage: 1,
      perPage: 10
    };
  },
  computed: {
    totalFaultPages() {
      return Math.ceil(this.faults.length / this.perPage);
    },
    totalPenaltyPages() {
      return Math.ceil(this.penalties.length / this.perPage);
    },
    paginatedFaults() {
      const start = (this.faultPage - 1) * this.perPage;
      return this.faults.slice(start, start + this.perPage);
    },
    paginatedPenalties() {
      const start = (this.penaltyPage - 1) * this.perPage;
      return this.penalties.slice(start, start + this.perPage);
    },
    faultPageNumbers() {
      const groupSize = 5;
      const start = Math.floor((this.faultPage - 1) / groupSize) * groupSize + 1;
      return Array.from({ length: Math.min(groupSize, this.totalFaultPages - start + 1) }, (_, i) => start + i);
    },
    penaltyPageNumbers() {
      const groupSize = 5;
      const start = Math.floor((this.penaltyPage - 1) / groupSize) * groupSize + 1;
      return Array.from({ length: Math.min(groupSize, this.totalPenaltyPages - start + 1) }, (_, i) => start + i);
    }

  },
  mounted() {
    this.fetchFaults();
    this.fetchPenalties();
  },
  methods: {
    formatDate(dateStr) {
      const date = new Date(dateStr);
      if (isNaN(date)) return 'Fecha inválida';
      return `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth() + 1).padStart(2, '0')}/${date.getFullYear()}`;
    },
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
.table th,
.table td {
  vertical-align: middle;
}

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

/* Círculo para números */
.pagination-container button:not(:first-child):not(:last-child):not([data-type="arrow"]) {
  border-radius: 50%;
}

/* Bordes redondeados para anterior/siguiente */
.pagination-container button:first-child,
.pagination-container button:last-child,
.pagination-container button[data-type="arrow"] {
  border-radius: 20px;
}

.header-box {
  background: linear-gradient(135deg, #28a745, #218838);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  border-left: 5px solid #1e7e34;
}

.nav-tabs .nav-link {
  border-radius: 10px 10px 0 0;
  transition: background-color 0.3s;
}

.nav-tabs .nav-link.active {
  background-color: #218838;
  color: white;
}

.nav-tabs .nav-link {
  color: black;
  /* Letras negras para pestañas inactivas */
}

.nav-tabs .nav-link.active {
  background-color: #218838;
  color: white;
}
</style>
