<template>
  <div>
    <div v-if="!isAuthenticated">
      <p>No estás autenticado. Por favor, inicia sesión.</p>
    </div>

    <div v-else>
      <div class="container">
        <h1 class="page-title">Gestión de Personal</h1> <!-- Título principal -->

        <!-- Formulario para agregar o editar personal -->
        <div v-if="isEditing || !person.id" class="card mt-4">
          <div class="card-body">
            <h5 class="card-title">{{ isEditing ? 'Editar' : 'Agregar' }} Personal</h5>
            
            <button @click="logout" class="btn btn-danger logout-button">Cerrar sesión</button>
            <br>
            <form @submit.prevent="isEditing ? updatePersonnel() : addPersonnel()">
              <div class="form-group">
                <label for="name">Nombre</label>
                <input v-model="person.name" type="text" class="form-control" id="name" placeholder="Nombre completo" required @blur="toUpperCase"/>
              </div><br>
              <div class="form-group">
                <label for="role">Cargo</label>
                <input v-model="person.role" type="text" class="form-control" id="role" placeholder="Cargo" required/>
              </div><br>
              <div class="form-group">
                <label for="id_area">Área</label>
                <select v-model="person.id_area" class="form-control" id="id_area" required>
                  <option v-for="area in areas" :key="area.id_area" :value="area.id_area">{{ area.name_area }}</option>
                </select>
              </div><br>
              <button type="submit" class="btn btn-success mr-2 action-button">{{ isEditing ? 'Actualizar' : 'Agregar' }}</button>
              <button type="button" class="btn btn-secondary action-button" @click="cancelEdit">Cancelar</button>
            </form>
          </div>
        </div>

        <h2 class="personnel-list-title">Lista de Personal</h2> <!-- Título de Lista de Personal -->
        <!-- Tarjeta de lista de personal con filtro -->
        <div class="card personnel-list-card">
          <div class="card-header">
            <input 
              v-model="searchQuery" 
              type="text" 
              class="form-control my-2" 
              placeholder="Buscar por nombre, cargo o área"
              @input="filterPersonnel"
            />
          </div>

          <div class="card-body">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Nombre</th>
                  <th>Cargo</th>
                  <th>Área</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(person, index) in paginatedPersonnel" :key="person.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ person.name }}</td>
                  <td>{{ person.role }}</td>
                  <td>{{ getAreaName(person.id_area) }}</td>
                  <td>
                    <button @click="editPersonnel(person)" class="btn btn-info action-button">Editar</button>
                    <button @click="deletePersonnel(person.id)" class="btn btn-danger action-button">Eliminar</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <nav aria-label="Page navigation" class="card-footer"><br>
            <ul class="pagination pagination-green justify-content-center">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="prevPage">Anterior</button>
              </li>
              <li v-for="page in visiblePages" :key="page" class="page-item" :class="{ active: page === currentPage }">
                <button class="page-link" @click="setPage(page)">{{ page }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link" @click="nextPage">Siguiente</button>
              </li>
            </ul>
          </nav>
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
      currentPage: 1,
      perPage: 10, // Número de elementos por página, ajustable
      searchQuery: '',
      pageGroupSize: 5, // Tamaño del grupo de páginas
    };
  },
  computed: {
    paginatedPersonnel() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.filteredPersonnel.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredPersonnel.length / this.perPage);
    },
    visiblePages() {
      const start = Math.floor((this.currentPage - 1) / this.pageGroupSize) * this.pageGroupSize + 1;
      const end = Math.min(start + this.pageGroupSize - 1, this.totalPages);
      let pages = [];
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
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
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    setPage(page) {
      this.currentPage = page;
    },
    toUpperCase() {
      this.person.name = this.person.name.toUpperCase();
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
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  text-align: center;
  margin-top: 20px;
}

.personnel-list-title {
  margin-top: 30px;
  font-size: 1.5rem;
}

/* Estilo para la barra de navegación */
.navbar-success {
  background-color: #019c54 !important;
  color: white;
}

/* Estilo para la tarjeta de la lista de personal */
.personnel-list-card {
  margin-top: 20px;
}

/* Estilo para el botón de cerrar sesión */
.logout-button {
  position: absolute;
  top: 17px;
  right: 17px;
}

/* Estilo para los botones de acción */
.action-button {
  margin-right: 5px;
}

/* Estilo para la barra de paginación */
.pagination-animated .page-link {
  color: #019c54;
  transition: background-color 0.3s ease;
}
.pagination-animated .page-link:hover {
  background-color: #019c54;
  color: #fff;
}

.pagination-green .page-link {
  color: white;
  background-color: #019c54;
  border: 1px solid #019c54;
  transition: background-color 0.3s ease;
}

.pagination-green .page-item.active .page-link {
  background-color: #019c35;
  border-color: #019c35;
}

</style>
