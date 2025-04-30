<template>
  <div>
    <div v-if="!isAuthenticated" class="text-center mt-5">
      <div class="alert alert-danger" role="alert">
        No estás autenticado. Por favor, inicia sesión.
      </div>
    </div>

    <div v-else class="container py-4">
      <h1 class="text-center mb-4 page-title">Gestión de Personal</h1>

      <!-- Formulario para agregar o editar personal -->
      <div v-if="isEditing || !person.id" class="card mb-5 shadow-sm">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0">{{ isEditing ? 'Editar Personal' : 'Agregar Personal' }}</h5>
          <button @click="logout" class="btn btn-danger">
            <i class="fas fa-sign-out-alt"></i> Cerrar sesión
          </button>
        </div>

        <div class="card-body">
          <form @submit.prevent="isEditing ? updatePersonnel() : addPersonnel()">
            <div class="form-group mb-3">
              <label for="name">Nombre</label>
              <input v-model="person.name" type="text" class="form-control" id="name" required
                @input="convertToUppercase('name')" />
            </div>

            <div class="form-group mb-3">
              <label for="role">Cargo</label>
              <input v-model="person.role" type="text" class="form-control" id="role" required
                @input="convertToUppercase('role')" />
            </div>


            <div class="form-group mb-4">
              <label for="id_area">Área</label>
              <select v-model="person.id_area" class="form-control" id="id_area" required>
                <option v-for="area in areas" :key="area.id_area" :value="area.id_area">
                  {{ area.name_area }}
                </option>
              </select>
            </div>

            <div class="d-flex justify-content-end">
              <button type="submit" class="btn btn-success me-2">
                <i class="fas fa-save"></i> {{ isEditing ? 'Actualizar' : 'Agregar' }}
              </button>
              <button type="button" class="btn btn-secondary" @click="cancelEdit">
                <i class="fas fa-times"></i> Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Lista de Personal -->
      <h2 class="text-center mb-3 personnel-list-title">Lista de Personal</h2>

      <div class="card shadow-sm">
        <div class="card-header">
          <input v-model="searchQuery" type="text" class="form-control" placeholder="Buscar por nombre, cargo o área"
            @input="filterPersonnel" />
        </div>

        <div class="card-body table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-secondary">
              <tr>
                <th>#</th>
                <th>Nombre</th>
                <th>Cargo</th>
                <th>Área</th>
                <th class="text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(person, index) in paginatedPersonnelList" :key="person.id">
                <td>{{ index + 1 }}</td>
                <td>{{ person.name }}</td>
                <td>{{ person.role }}</td>
                <td>{{ getAreaName(person.id_area) }}</td>
                <td class="text-center">
                  <div class="dropdown">
                    <button class="btn btn-sm border-0 bg-transparent p-0" type="button" data-bs-toggle="dropdown"
                      aria-expanded="false">
                      <i class="fas fa-ellipsis-v"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                      <li>
                        <button class="dropdown-item" @click="editPersonnel(person)">
                          <i class="fas fa-edit me-2"></i> Editar
                        </button>
                      </li>
                      <li>
                        <button class="dropdown-item" @click="deletePersonnel(person.id)">
                          <i class="fas fa-trash-alt me-2"></i> Eliminar
                        </button>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div class="card-footer text-center">
          <div class="pagination-container mt-4 d-flex justify-content-center align-items-center gap-2">

            <!-- Botón Anterior -->
            <button @click="prevPage" class="pagination-btn" :disabled="currentPage === 1">
              Anterior
            </button>

            <ul class="pagination mb-0 d-flex gap-1">
              <!-- Páginas visibles -->
              <li v-for="page in visiblePages" :key="page" class="page-item-custom"
                :class="{ active: page === currentPage }">
                <button @click="setPage(page)" class="page-link-custom"
                  :class="{ 'active-page': page === currentPage }">
                  {{ page }}
                </button>
              </li>
            </ul>

            <!-- Botón Siguiente -->
            <button @click="nextPage" class="pagination-btn" :disabled="currentPage === totalPages">
              Siguiente
            </button>
          </div><br>
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
    const router = useRouter(); // Obtenemos el enrutador en el contexto de `setup`

    return {
      router
    };
  },
  data() {
    return {
      isAuthenticated: false,
      personnelList: [],
      person: { id: '', name: '', role: '', id_area: '' },
      roles: [],
      areas: [],
      isEditing: false,
      searchQuery: '',
      pageGroupSize: 3, // Tamaño del grupo de páginas
      currentPage: 1, // Página actual
      pagesPerPage: 10, // Elementos por página
      groupStartPage: 1, // Página de inicio del grupo de páginas visibles
    };
  },
  computed: {
    // Número total de páginas
    totalPages() {
      if (!Array.isArray(this.personnelList)) return 0;
      return Math.ceil(this.personnelList.length / this.pagesPerPage);
    },
    // Páginas visibles agrupadas de 3 en 3
    visiblePages() {
      const pages = [];
      let groupEndPage = this.groupStartPage + 2; // Solo mostrar 3 páginas

      // Asegura que no sobrepasemos el total de páginas
      if (groupEndPage > this.totalPages) {
        groupEndPage = this.totalPages;
      }

      for (let i = this.groupStartPage; i <= groupEndPage; i++) {
        pages.push(i);
      }
      return pages;
    },
    // Elementos por página
    paginatedPersonnelList() {
      const start = (this.currentPage - 1) * this.pagesPerPage;
      const end = this.currentPage * this.pagesPerPage;
      return this.filteredPersonnel.slice(start, end);
    },

    filteredPersonnel() {
      return this.personnelList
        .filter(person => {
          const name = person.name.toLowerCase();
          const role = person.role.toLowerCase();
          const area = this.getAreaName(person.id_area).toLowerCase();
          const query = this.searchQuery.toLowerCase();
          return name.includes(query) || role.includes(query) || area.includes(query);
        })
        .sort((a, b) => a.name.localeCompare(b.name)); // Orden alfabético por nombre
    }
  },
  methods: {
    async fetchPersonnel() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-personnel`);
        const personnelData = response.data.personnel || [];
        this.personnelList = personnelData.map(person => ({
          id: person[0],
          name: person[1],
          role: person[2],
          id_area: person[3]
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
      const area = this.areas.find(area => area.id_area === areaId);
      return area ? area.name_area : 'Área desconocida';
    },
    async addPersonnel() {
      try {
        console.log('Datos a enviar:', this.person);  // Verifica los datos antes de enviarlos
        await axios.post(`${process.env.VUE_APP_API_URL}/api/add-personnel`, this.person);
        alert('Usuario añadido exitosamente.');
        this.fetchPersonnel();  // Refresca la lista de personal
        this.resetForm();  // Resetea el formulario
      } catch (error) {
        console.error('Error al añadir personal:', error);
      }
    },
    editPersonnel(person) {
      this.person = { ...person };
      this.isEditing = true;
      window.scrollTo({ top: 0, behavior: 'smooth' }); // Desplazamiento al tope
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
      // Solicitar confirmación antes de eliminar
      const confirmation = window.confirm('¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.');

      // Proceder solo si el usuario confirma
      if (confirmation) {
        try {
          await axios.delete(`${process.env.VUE_APP_API_URL}/api/delete-personnel/${id}`);
          alert('Usuario eliminado exitosamente.');
          this.fetchPersonnel(); // Refrescar la lista de personal después de eliminar
        } catch (error) {
          console.error('Error al eliminar personal:', error);
        }
      } else {
        alert('Eliminación cancelada.');
      }
    },
    cancelEdit() {
      this.resetForm();
    },
    resetForm() {
      this.person = { id: '', name: '', role: '', id_area: '' };
      this.isEditing = false;
    },
    filterPersonnel() {
      this.currentPage = 1;
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.updatePageGroup();
      }
    },
    // Función para ir a la siguiente página
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.updatePageGroup();
      }
    },
    // Función para cambiar de página
    setPage(page) {
      this.currentPage = page;
      this.updatePageGroup();
    },
    // Función para actualizar el grupo de páginas visibles
    updatePageGroup() {
      if (this.currentPage <= this.groupStartPage) {
        this.groupStartPage = Math.max(1, this.currentPage - 1); // Asegura que no baje de 1
      } else if (this.currentPage > this.groupStartPage + 2) {
        this.groupStartPage = this.currentPage - 2;
      }
    },
    convertToUppercase(field) {
      this.person[field] = this.person[field].toUpperCase();
    },
    logout() {
      // Eliminamos el token de autenticación
      localStorage.removeItem('authToken');
      this.isAuthenticated = false;

      // Redirigimos a la página de inicio de sesión
      this.router.push('/login'); // Cambia '/login' por la ruta que uses para el inicio de sesión
    },
    checkAuthentication() {
      const token = localStorage.getItem('authToken');
      if (token) {
        this.isAuthenticated = true;
      } else {
        // Redirigimos a la página de inicio de sesión si no está autenticado
        this.router.push('/login');
      }
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
.dropdown-menu {
  min-width: 8rem;
  /* Opcional, tamaño mínimo del menú */
}

.dropdown-item {
  font-size: 0.9rem;
}

.dropdown-item i {
  width: 18px;
  /* Hace que todos los iconos tengan el mismo espacio reservado */
  text-align: center;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  text-align: center;
  margin-top: 20px;
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
  max-width: 1200px;
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

/* Barra de paginación */


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

/* Estilos para la paginación */
.pagination-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Botones de Anterior y Siguiente */
.pagination-btn {
  background-color: #fff;
  color: #198754;
  border: 2px solid #198754;
  padding: 6px 14px;
  border-radius: 20px;
  transition: all 0.3s ease;
  font-weight: 600;
}

/* Hover en los botones */
.pagination-btn:hover:not(:disabled) {
  background-color: #198754;
  color: #fff;
  box-shadow: 0 4px 12px rgba(25, 135, 84, 0.3);
}

/* Botones deshabilitados */
.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Estilo de los elementos de las páginas */
.page-item-custom {
  list-style: none;
}

/* Estilo de los botones de las páginas */
.page-link-custom {
  border: 2px solid #198754;
  background-color: #f8f9fa;
  color: #198754;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

/* Hover sobre los botones de las páginas */
.page-link-custom:hover {
  background-color: #d1e7dd;
  color: #0f5132;
  cursor: pointer;
}

/* Página activa */
.active-page {
  background-color: #198754;
  color: #fff;
  font-weight: bold;
  box-shadow: 0 0 8px rgba(25, 135, 84, 0.5);
}
</style>
