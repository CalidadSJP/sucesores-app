<template>
  <div class="container mt-4">
    <h1 class="mb-4">Gestión de Personal</h1>

    <!-- Formulario para Agregar o Editar Personal -->
    <div class="card mb-4">
      <div class="card-header d-flex justify-content-between align-items-center">
      <!-- Título de la tarjeta a la izquierda -->
      <span>
        {{ isEditing ? 'Editar Personal' : 'Agregar Nuevo Personal' }}
      </span>

      <!-- Botón de regresar a la derecha -->
      <router-link to="/" class="back-link d-flex align-items-center">
        <img
          src="@/assets/home.png"
          alt="Regresar"
          class="back-icon"
          style="width: 20px; height: 20px; margin-right: 5px;"
        />
        <span class="card-text">Inicio</span>
      </router-link>
    </div>
      <div class="card-body">
          <form @submit.prevent="isEditing ? updatePersonnel() : addPersonnel()">
      <div class="mb-3">
          <label for="name" class="form-label">Nombre</label>
          <input type="text" id="name" v-model="person.name" @input="toUpperCase($event)" class="form-control" placeholder="Nombre" required />
      </div>
      <div class="mb-3">
          <label for="role" class="form-label">Cargo</label>
          <input type="text" id="role" v-model="person.role" @input="toUpperCase($event)" class="form-control"  placeholder="Cargo" required />
      </div>

    <div class="mb-3">
      <label for="area" class="form-label">Área</label>
      <select id="area" v-model="person.id_area" class="form-select" required>
        <option v-for="area in areas" :key="area.id_area" :value="area.id_area">{{ area.name_area }}</option>
      </select>
    </div><br>
    <div>
      <button type="submit" class="btn btn-success">{{ isEditing ? 'Actualizar' : 'Agregar' }}</button>
      <button v-if="isEditing" @click="cancelEdit" class="btn btn-secondary ms-2">Cancelar</button>
    </div>
  </form>
</div>
</div>


    <!-- Listado de Personal -->
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
          <span>Lista de Personal</span>
          <button class="btn btn-success" type="button" data-bs-toggle="collapse" data-bs-target="#filterCollapse" aria-expanded="false" aria-controls="filterCollapse">
              Filtros
          </button>
      </div>
      <div class="collapse" id="filterCollapse">
          <div class="card-body p-4">
              <input v-model="search.name" @input="toUpperCase($event)" class="form-control mb-3" placeholder="Buscar por nombre" />
              <input v-model="search.role" @input="toUpperCase($event)" class="form-control mb-3" placeholder="Buscar por cargo" />
              <input v-model="search.area" @input="toUpperCase($event)" class="form-control mb-3" placeholder="Buscar por área" />
          </div>
      </div>
      <div class="card-body p-4">
      <div class="table-responsive">
          <table class="table table-striped table-hover mb-3">
              <thead class="table-light">
                  <tr>
                      <th>Nombre</th>
                      <th>Cargo</th>
                      <th>Área</th>
                      <th>Acciones</th>
                  </tr>
              </thead>
      <tbody>
        <tr v-for="item in paginatedPersonnelList" :key="item.id">
          <td>{{ item.name }}</td>
          <td>{{ item.role }}</td>
          <td>{{ areaName(item.id_area) }}</td>
          <td>
            <button @click="editPersonnel(item)" class="btn btn-secondary btn-sm me-2">Editar</button>
            <button @click="deletePersonnel(item.id)" class="btn btn-danger btn-sm">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- Paginación -->
  <nav aria-label="Page navigation">
      <ul class="pagination justify-content-center mb-0">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a class="page-link btn-success text-white" @click="prevPage">Anterior</a>
        </li>
        <li
          class="page-item"
          :class="{ active: page === currentPage }"
          v-for="page in visiblePages"
          :key="page"
        >
          <a class="page-link btn-success text-white" @click="setPage(page)">{{ page }}</a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <a class="page-link btn-success text-white" @click="nextPage">Siguiente</a>
        </li>
      </ul>
    </nav>
</div>
</div>
</div>
</template>

<script>
import axios from 'axios';

export default {
data() {
  return {
    personnelList: [],
    person: { id: '', name: '', role: '', id_area: '' },
    roles: [],
    areas: [],
    isEditing: false,
    search: {
      name: '',
      role: '',
      area: ''
    },
    currentPage: 1,
    perPage: 10,
  };
},
computed: {
  visiblePages() {
    const pages = [];
    const startPage = Math.max(1, this.currentPage - 2);
    const endPage = Math.min(this.totalPages, startPage + 4);

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }

    return pages;
  },
  filteredPersonnelList() {
    return this.personnelList.filter(item => {
      return (
        (!this.search.name || item.name.toLowerCase().includes(this.search.name.toLowerCase())) &&
        (!this.search.role || item.role.toLowerCase().includes(this.search.role.toLowerCase())) &&
        (!this.search.area || this.areaName(item.id_area).toLowerCase().includes(this.search.area.toLowerCase()))
      );
    });
  },
  sortedFilteredPersonnelList() {
    return this.filteredPersonnelList
      .slice()  // Create a copy of the filtered list
      .sort((a, b) => a.name.localeCompare(b.name));  // Sort alphabetically by name
  },
  paginatedPersonnelList() {
    const start = (this.currentPage - 1) * this.perPage;
    const end = start + this.perPage;
    return this.sortedFilteredPersonnelList.slice(start, end);
  },
  totalPages() {
    return Math.ceil(this.sortedFilteredPersonnelList.length / this.perPage);
  }
},
methods: {
  async fetchPersonnel() {
    try {
      const response = await axios.get(`${process.env.VUE_APP_API_URL}/get-personnel`);
      this.personnelList = response.data.personnel;
    } catch (error) {
      console.error('Error al obtener el personal:', error);
    }
  },
  async fetchRoles() {
    try {
      const response = await axios.get(`${process.env.VUE_APP_API_URL}/get-roles`);
      this.roles = response.data.roles;
    } catch (error) {
      console.error('Error al obtener los roles:', error);
    }
  },
  async fetchAreas() {
    try {
      const response = await axios.get(`${process.env.VUE_APP_API_URL}/get-areas`);
      this.areas = response.data.areas;
    } catch (error) {
      console.error('Error al obtener las áreas:', error);
    }
  },
  async addPersonnel() {
    if (confirm('¿Estás seguro de que deseas agregar este usuario?')) {
      try {
        await axios.post(`${process.env.VUE_APP_API_URL}/add-personnel`, this.person);
        alert('Usuario agregado exitosamente.');
        this.fetchPersonnel();
        this.person = { id: '', name: '', role: '', id_area: '' };
        this.isEditing = false;
      } catch (error) {
        console.error('Error al agregar personal:', error);
      }
    }
  },
  editPersonnel(person) {
    this.person = { ...person };
    this.isEditing = true;
    this.scrollToTop();
  },
  async updatePersonnel() {
    if (confirm('¿Estás seguro de que deseas editar este usuario?')) {
      try {
        await axios.put(`${process.env.VUE_APP_API_URL}/update-personnel`, this.person);
        alert('Usuario actualizado exitosamente.');
        this.fetchPersonnel();
        this.cancelEdit();
      } catch (error) {
        console.error('Error al actualizar personal:', error);
      }
    }
  },
  cancelEdit() {
    this.person = { id: '', name: '', role: '', id_area: '' };
    this.isEditing = false;
  },
  async deletePersonnel(id) {
    if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
      try {
        await axios.delete(`${process.env.VUE_APP_API_URL}/delete-personnel/${id}`);
        alert('Usuario eliminado exitosamente.');
        this.fetchPersonnel();
      } catch (error) {
        console.error('Error al eliminar personal:', error);
      }
    }
  },
  areaName(id) {
    const area = this.areas.find(area => area.id_area === id);
    return area ? area.name_area : 'Desconocida';
  },
  setPage(page) {
    this.currentPage = page;
  },
  nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  },
  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  },
  scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  },
  toUpperCase(event) {
    event.target.value = event.target.value.toUpperCase();
  }
},
mounted() {
  this.fetchPersonnel();
  this.fetchRoles();
  this.fetchAreas();
}
};
</script>

<style scoped>

.card-body {
  padding: 1.5rem; /* Mayor espacio en el contenedor */
}

.table td, .table th {
  padding: 1rem; /* Mayor espacio en las celdas de la tabla */
}

.table {
  margin-bottom: 1rem; /* Espacio inferior para la tabla */
}

.input, .form-control {
  margin-bottom: 1rem; /* Espacio entre los campos de entrada */
}

.pagination {
  margin-top: 2rem; /* Espacio superior para la paginación */
}

.page-link {
  cursor: pointer;
}

.page-link-animation {
  transition: background-color 0.3s, transform 0.3s;
}

.page-link:hover {
  background-color: #e9ecef; /* Color de fondo al pasar el mouse */
}

.pagination .page-link {
background-color: #28a745; /* Color verde de btn-success */
color: white;
border: 1px solid #28a745;
padding: 0.5rem 0.75rem;
font-size: 0.875rem;

}

.pagination .page-link:hover {
background-color: #218838; /* Color verde oscuro al pasar el mouse */
color: white;
}

.pagination .page-item.active .page-link {
background-color: #218838; /* Color verde oscuro para la página activa */
border-color: #218838;
}

h1{
font-weight: bold;
}

span{
font-weight: bold;
}

.card-text {
font-size: 23px; /* Ajusta el tamaño de la palabra según sea necesario */
color: #000; /* Ajusta el color de la palabra según sea necesario */

}

.back-link {
text-decoration: none; /* Elimina el subrayado del enlace */
}
</style>
