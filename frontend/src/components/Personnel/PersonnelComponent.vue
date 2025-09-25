<template>
  <div>
    <div v-if="isAuthenticated" class="container-fluid py-4">
      <h3 class="text-center mb-1 page-title">Gestión de Personal</h3>
      <div class="row d-flex align-items-stretch"> <!-- Columna izquierda: Formulario -->
        <div class="col-md-5">
          <div class="card shadow-sm card-form">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">{{ isEditing ? 'Editar Personal' : 'Agregar Personal' }}</h5> <button @click="logout"
                class="btn btn-danger btn-sm"> <i class="fas fa-sign-out-alt"></i> Salir </button>
            </div>
            <div class="card-body">
              <form @submit.prevent="isEditing ? updatePersonnel() : addPersonnel()">
                <div class="form-group mb-3"> <label for="last_name">Apellidos</label> <input v-model="person.last_name"
                    type="text" class="form-control" id="last_name" required @input="updateFullName" /> </div>
                <div class="form-group mb-3"> <label for="first_name">Nombres</label> <input v-model="person.first_name"
                    type="text" class="form-control" id="first_name" required @input="updateFullName" /> </div>
                <div class="form-group mb-3"> <label for="identifier">Cédula</label> <input v-model="person.identifier"
                    type="text" class="form-control" id="identifier" required maxlength="10" /> </div>
                <div class="form-group mb-3"> <label for="role">Cargo</label> <input v-model="person.role" type="text"
                    class="form-control" id="role" required @input="convertToUppercase('role')" /> </div>
                <div class="form-group mb-4"> <label for="id_area">Área</label> <select v-model="person.id_area"
                    class="form-control" id="id_area" required>
                    <option v-for="area in areas" :key="area.id_area" :value="area.id_area"> {{ area.name_area }}
                    </option>
                  </select> </div>
                <div class="d-flex justify-content-end"> <button type="submit" class="btn btn-success me-2"> <i
                      class="fas fa-save"></i> {{ isEditing ? 'Actualizar' : 'Agregar' }} </button> <button
                    type="button" class="btn btn-secondary" @click="cancelEdit"> <i class="fas fa-times"></i> Cancelar
                  </button> </div>
              </form>
            </div>
          </div>
        </div> <!-- Columna derecha: Lista de nombres -->
        <div class="col-md-5">
          <div class="card shadow-sm card-list">
            <div class="card-header"> <input v-model="searchQuery" type="text" class="form-control"
                placeholder="Buscar por nombre, cédula, cargo o área..." @input="filterPersonnel" /> </div>
            <div class="card-body list-group" style="max-height: 600px; overflow-y: auto;"> <button
                v-for="person in filteredPersonnel" :key="person.id" class="list-group-item list-group-item-action"
                @click="selectPerson(person)"> {{ person.name }} </button> </div>
          </div>
        </div>
      </div> <!-- Tarjeta flotante (modal overlay) -->
      <div v-if="selectedPerson" class="overlay">
        <div class="modal-card">
          <div class="modal-header">
            <h5>{{ selectedPerson.name }}</h5> <button class="btn-close" @click="selectedPerson = null"></button>
          </div>
          <div class="modal-body">
            <p><strong>Cédula:</strong> {{ selectedPerson.identifier }}</p>
            <p><strong>Cargo:</strong> {{ selectedPerson.role }}</p>
            <p><strong>Área:</strong> {{ getAreaName(selectedPerson.id_area) }}</p>
          </div>
          <div class="modal-footer d-flex justify-content-between">
            <div> <button class="btn btn-primary me-2" @click="editPersonnel(selectedPerson)"> <i
                  class="fas fa-edit"></i> Editar </button> <button class="btn btn-danger"
                @click="deletePersonnel(selectedPerson.id)"> <i class="fas fa-trash"></i> Eliminar </button> </div>
            <button class="btn btn-secondary" @click="selectedPerson = null"> <i class="fas fa-times"></i> Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter(); // Obtenemos el enrutador en setup
    return { router };
  },

  data() {
    return {
      isAuthenticated: false,
      personnelList: [],
      person: {
        id: '',
        last_name: '',
        first_name: '',
        identifier: '',
        role: '',
        id_area: '',
        name: '' // se llena automáticamente
      },
      roles: [],
      areas: [],
      isEditing: false,
      searchQuery: '',
      pageGroupSize: 3,
      currentPage: 1,
      pagesPerPage: 10,
      groupStartPage: 1,
      selectedPerson: null
    };
  },

  computed: {
    filteredPersonnel() {
      const query = this.searchQuery.toLowerCase();
      return this.personnelList
        .filter(person => {
          const name = person.name?.toLowerCase() || '';
          const role = person.role?.toLowerCase() || '';
          const area = this.getAreaName(person.id_area).toLowerCase();
          const identifier = person.identifier ? String(person.identifier).toLowerCase() : '';
          return name.includes(query) || identifier.includes(query) || role.includes(query) || area.includes(query);
        })
        .sort((a, b) => a.name.localeCompare(b.name));
    }
  },

  methods: {
    // Selección de persona
    selectPerson(person) {
      this.selectedPerson = person;
    },

    // Actualizar nombre completo
    updateFullName() {
      const last = this.person.last_name?.toUpperCase().trim() || '';
      const first = this.person.first_name?.toUpperCase().trim() || '';
      this.person.name = `${last} ${first}`.trim();
    },

    // Fetch data
    async fetchPersonnel() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-personnel`);
        const personnelData = response.data.personnel || [];
        this.personnelList = personnelData.map(p => ({
          id: p[0],
          name: p[1],
          role: p[2],
          id_area: p[3],
          identifier: p[4]
        }));
      } catch (error) {
        console.error('Error al obtener el personal:', error);
      }
    },

    async fetchRoles() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-roles`);
        this.roles = response.data;
      } catch (error) {
        console.error('Error al obtener los roles:', error);
      }
    },

    async fetchAreas() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-areas`);
        const areasData = response.data.areas || [];
        this.areas = areasData.map(area => ({
          id_area: area[0],
          name_area: area[1]
        }));
      } catch (error) {
        console.error('Error al obtener áreas:', error);
      }
    },

    getAreaName(areaId) {
      const area = this.areas.find(a => a.id_area === areaId);
      return area ? area.name_area : 'Área desconocida';
    },

    // CRUD
    async addPersonnel() {
      try {
        console.log('Datos a enviar:', this.person);
        await axios.post(`${process.env.VUE_APP_API_URL}/api/add-personnel`, this.person);
        alert('Usuario añadido exitosamente.');
        this.fetchPersonnel();
        this.resetForm();
      } catch (error) {
        console.error('Error al añadir personal:', error);
      }
    },

    editPersonnel(person) {
      this.person = { ...person };
      if (this.person.name) {
        const parts = this.person.name.trim().split(' ');
        this.person.last_name = parts.slice(0, 2).join(' ') || '';
        this.person.first_name = parts.slice(2).join(' ') || '';
      }
      this.isEditing = true;
      this.selectedPerson = null;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    async updatePersonnel() {
      try {
        await axios.put(`${process.env.VUE_APP_API_URL}/api/update-personnel/${this.person.id}`, this.person);
        alert('Usuario actualizado exitosamente.');
        this.fetchPersonnel();
        this.resetForm();
      } catch (error) {
        console.error('Error al actualizar personal:', error);
      }
    },

    async deletePersonnel(id) {
      const confirmation = window.confirm('¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.');
      if (!confirmation) return alert('Eliminación cancelada.');

      try {
        await axios.delete(`${process.env.VUE_APP_API_URL}/api/delete-personnel/${id}`);
        alert('Usuario eliminado exitosamente.');
        this.fetchPersonnel();
        this.selectedPerson = null;
        this.searchQuery = '';
      } catch (error) {
        console.error('Error al eliminar personal:', error);
      }
    },

    cancelEdit() {
      this.resetForm();
    },

    resetForm() {
      this.person = {
        id: '',
        last_name: '',
        first_name: '',
        identifier: '',
        role: '',
        id_area: '',
        name: ''
      };
      this.isEditing = false;
    },

    filterPersonnel() {
      this.currentPage = 1;
    },

    convertToUppercase(field) {
      this.person[field] = this.person[field]?.toUpperCase();
    },

    logout() {
      localStorage.removeItem('authToken');
      this.isAuthenticated = false;
      this.router.push('/control-home');
    },

    checkAuthentication() {
      const token = localStorage.getItem('authToken');
      if (token) this.isAuthenticated = true;
      else this.router.push('/login/Talento Humano');
    }
  },

  mounted() {
    this.checkAuthentication();
    if (this.isAuthenticated) {
      this.fetchPersonnel();
      this.fetchRoles();
      this.fetchAreas();
    }
  }
};
</script>



<style scoped>
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  color: #019c54;
}

.personnel-list-title {
  text-align: center;
  margin-top: 30px;
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
}

/* Barra de navegación (si la usas) */
.navbar-success {
  background-color: #019c54 !important;
  color: white;
}

/* Tarjeta de la lista de personal */
.card {
  margin-top: 20px;
}

.my-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* Botón de cerrar sesión */
.logout-button {
  position: absolute;
  top: 17px;
  right: 17px;
}

/* Botones de acción */
.action-button {
  margin-right: 5px;
}

/* Botones generales */
.btn {
  font-weight: 500;
}

/* Botones específicos de acción (Editar/Eliminar) */
.btn-info {
  background-color: #17a2b8;
  border-color: #17a2b8;
}

.btn-info:hover {
  background-color: #138496;
  border-color: #117a8b;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

/* Inputs */
.form-control {
  font-weight: 400 !important;
  border-radius: 0.5rem;
}

/* Tabla de personal */
.table {
  font-size: 0.95rem;
}

.table-hover tbody tr:hover {
  background-color: #e6f9ef;
}

/* Estilo para los íconos */
i {
  margin-right: 5px;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-card {
  background: #fff;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease-in-out;
}

.modal-header,
.modal-footer {
  padding: 15px;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-footer {
  border-top: 1px solid #dee2e6;
}

.modal-body {
  padding: 15px;
}

.btn-close {
  border: none;
  background: transparent;
  font-size: 1.2rem;
}

.row {
  display: flex;
  justify-content: center;
  gap: 10px;
  /* separación entre tarjetas */
}

.col-lg-5 {
  display: flex;
  flex-direction: column;
}

/* Tarjeta de formulario */
.card-form {
  max-height: 515px;
  /* Ajusta según lo que se vea bien */
}

/* Tarjeta de lista */
.card-list {
  max-height: 515px;
  /* Igual que la de formulario */
  overflow-y: auto;
  /* Mantiene el scroll interno */
}
</style>
