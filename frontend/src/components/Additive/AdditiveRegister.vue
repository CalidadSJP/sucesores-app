<template>
  <h1 class="text-center mb-4">Registro - Ingreso a Bodega de Aditivos</h1>
  <div class="container-fluid p-4 d-flex justify-content-center">
    <div class="card">
      <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
        <h4>Tabla Editable</h4>
        <div>
          <button @click="$router.push('/additive-release')" class="btn btn-warning me-2">
            <i class="fas fa-outdent"></i> Liberación
          </button>
          <button @click="logout" class="btn btn-danger">
            <i class="fas fa-sign-out-alt"></i> Cerrar sesión
          </button>
        </div>
      </div>

      <div class="card-body">
        <!-- Filtro de búsqueda -->
        <div class="mb-3">
          <input type="text" v-model="searchQuery" placeholder="Buscar..." class="form-control" />
        </div>

        <div class="table-responsive">
          <table class="table table-bordered table-striped">
            <thead>
              <tr>
                <th v-for="(header, index) in headers" :key="header" :class="['text-nowrap', stickyClass(index)]">
                  {{ header }}
                </th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in paginatedData" :key="row.id">
                <td v-for="(key, index) in keys" :key="key" :class="['text-nowrap', stickyClass(index)]">
                  <input v-if="editableRow === index" :value="row[key]"
                    @input="row[key] = $event.target.value.toUpperCase()" class="form-control" type="text" />
                  <span v-else>{{ row[key] }}</span>
                </td>
                <td>
                  <button v-if="editableRow === index" class="btn btn-success btn-sm ms-1" @click="saveRow(index)">
                    Guardar
                  </button>
                  <button v-else class="btn btn-info btn-sm mb-1 mt-1 ms-1" @click="editRow(index)">
                    Editar
                  </button>
                  <button class="btn btn-danger btn-sm mt-1 mb-1 ms-1" @click="deleteRow(row.id)">
                    Eliminar
                  </button>
                  <a v-if="shouldShowRedirectButton(row)" class="btn btn-warning btn-sm ms-1 mt-1 mb-1"
                    :href="'/additive-files'">
                    Subir Archivo
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <nav aria-label="Paginación" class="d-flex justify-content-center mt-4">
          <ul class="pagination">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <button class="page-link bg-success text-white border-success" @click="currentPage--">Anterior</button>
            </li>
            <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
              <button class="page-link" @click="currentPage = page"
                :class="currentPage === page ? 'active-page' : 'bg-success text-white border-success'">
                {{ page }}
              </button>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <button class="page-link bg-success text-white border-success" @click="currentPage++">Siguiente</button>
            </li>
          </ul>
        </nav>

        <button class="btn btn-success mt-3" @click="downloadExcel">
          Descargar Registro
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      headers: [
        "ID",
        "Fecha de Entrada",
        "Producto",
        "Proveedor",
        "Nombre del Conductor",
        "ID del Conductor",
        "Permiso Transporte Alimentos",
        "Validez Transporte Alimentos",
        "Registro Fumigación",
        "Última Fumigación",
        "Número Factura",
        "Olores Extraños",
        "Evidencia Plagas",
        "Camión Limpio",
        "Personal Uniformado",
        "Condición Paredes/Suelo/Techo",
        "Huecos en Caja Camión",
        "Sticker Desinfección",
        "Cuerpos Extraños",
        "Número de Lote",
        "Cantidad de Paquetes",
        "Peso Total",
        "Fecha de Fabricación",
        "Fecha de Expiración",
        "Revisión Vida Útil",
        "Declaración Alergénicos",
        "Sistema Gráfico",
        "Producto Aceptado",
        "Razones de Rechazo",
        "Recibido Por",
        "Factura/Guía de remisión",
        "Imagen de condición del camión",
        "Imagen de la Placa del Camión",
        "Ficha Técnica/Certificado de Calidad",
        "Liberacion"
      ],
      keys: [
        "id",
        "entry_date",
        "product",
        "supplier",
        "driver_name",
        "driver_id",
        "food_transport_permission",
        "food_transport_validity",
        "fumigation_record",
        "last_fumigation_date",
        "invoice_number",
        "strange_smells",
        "pests_evidence",
        "clean_truck",
        "uniformed_personnel",
        "floor_walls_roof_condition",
        "truck_box_holes",
        "disinfection_sticker",
        "foreign_bodies",
        "lot_number",
        "package_quantity",
        "total_weight",
        "manufacture_date",
        "expiry_date",
        "shelf_life_check",
        "allergen_statement",
        "graphic_system",
        "product_accepted",
        "rejection_reasons",
        "received_by",
        "invoice_file_confirmation",
        "truck_condition_image_confirmation",
        "truck_plate_image_confirmation",
        "technical_file_confirmation",
        "liberation"
      ],
      tableData: [],
      editableRow: null,
      searchQuery: "",
      currentPage: 1,
      itemsPerPage: 10,
    };
  },
  computed: {
    // Filtrar datos basado en la búsqueda
    filteredData() {
      if (!this.searchQuery) {
        return this.tableData;
      }
      const query = this.searchQuery.toLowerCase();
      return this.tableData.filter((row) =>
        Object.values(row).some((value) =>
          String(value).toLowerCase().includes(query)
        )
      );
    },
    // Paginar los datos filtrados
    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredData.slice(start, end);
    },
    // Calcular total de páginas
    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage);
    },
  },
  methods: {
    fetchTableData() {
      axios
        .get(`${process.env.VUE_APP_API_URL}/api/products`)
        .then((response) => {
          this.tableData = response.data;

          // Formatear las fechas en el formato yyyy-mm-dd para su visualización en la tabla
          this.tableData.forEach((row) => {
            if (row.entry_date) {
              row.entry_date = this.formatDate(row.entry_date);
            }
            if (row.last_fumigation_date) {
              row.last_fumigation_date = this.formatDate(row.last_fumigation_date);
            }
            if (row.manufacture_date) {
              row.manufacture_date = this.formatDate(row.manufacture_date);
            }
            if (row.expiry_date) {
              row.expiry_date = this.formatDate(row.expiry_date);
            }
          });

          this.tableData.sort((a, b) => b.id - a.id); // Orden descendente por ID
        })
        .catch((error) => {
          console.error("Error al obtener los datos:", error);
        });
    },

    formatDate(dateString) {
      // Crear un objeto de fecha a partir de la cadena recibida
      const date = new Date(dateString);

      // Sumar 1 al día para ajustar el desfase (si es necesario)
      date.setDate(date.getDate() + 1);

      // Obtener el año, mes y día en el formato yyyy-mm-dd
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");

      // Devolver la fecha en formato yyyy-mm-dd
      return `${year}-${month}-${day}`;
    },

    editRow(index) {
      this.editableRow = index;
    },

    saveRow(index) {
      const updatedRow = this.tableData[index];

      // Las fechas ya están en el formato correcto, no es necesario hacer nada aquí
      axios
        .put(`${process.env.VUE_APP_API_URL}/api/products/${updatedRow.id}`, updatedRow)
        .then(() => {
          this.editableRow = null;
          this.fetchTableData(); // Volver a obtener los datos y ordenarlos
        })
        .catch((error) => {
          console.error("Error al actualizar el registro:", error);
        });
    },

    deleteRow(id) {
      // Mostrar el mensaje de confirmación
      const confirmDelete = window.confirm("¿Estás seguro de que deseas eliminar este registro?");

      if (confirmDelete) {
        // Si el usuario confirma, realizar la eliminación
        axios
          .delete(`${process.env.VUE_APP_API_URL}/api/products/${id}`)
          .then(() => {
            this.fetchTableData(); // Volver a cargar los datos después de la eliminación
          })
          .catch((error) => {
            console.error("Error al eliminar el registro:", error);
          });
      } else {
        // Si el usuario cancela, no hacer nada
        console.log("Eliminación cancelada");
      }
    },

    downloadExcel() {
      axios({
        url: `${process.env.VUE_APP_API_URL}/api/download-product-table`,
        method: 'GET',
        responseType: 'blob', // Importante para manejar archivos binarios
      })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'registro-aditivos.xlsx');
          document.body.appendChild(link);
          link.click();
          link.remove();
        })
        .catch((error) => {
          console.error("Error al descargar el archivo:", error);
          alert("Ocurrió un error al intentar descargar el archivo.");
        });
    }
    ,
    shouldShowRedirectButton(row) {
      // Mostrar el botón de enlace solo si alguna columna de confirmación tiene 'NO'
      return (
        row.invoice_file_confirmation === "NO" ||
        row.truck_condition_image_confirmation === "NO" ||
        row.truck_plate_image_confirmation === "NO" ||
        row.technical_file_confirmation === "NO"
      );
    },

    logout() {
      // Limpia el almacenamiento local y redirige al usuario
      localStorage.removeItem('authToken'); // Elimina el token
      localStorage.removeItem('user_area'); // Elimina el área
      localStorage.removeItem('user_id'); // Elimina el ID del usuario
      this.$router.push('/additive-login'); // Redirige al login
    },
    stickyClass(index) {
      if (index === 0) return 'sticky-col-0';
      if (index === 1) return 'sticky-col-1';
      if (index === 2) return 'sticky-col-2';
      return '';
    }
  }
  ,
  mounted() {
    this.fetchTableData();
  }
};
</script>

<style scoped>
.container-fluid {
  max-width: 100%;
  /* Asegura que ocupe toda la pantalla */
  margin: 0;
  /* Elimina márgenes predeterminados */
  padding: 0;
  /* Relleno de la pantalla */
}

.card {
  padding: 5px;
  /* Relleno dentro de la tarjeta */
  max-width: 1400px;
}

.table {
  width: 100%;
  table-layout: auto;
  /* Permite que las celdas se ajusten automáticamente al contenido */
  margin-top: 20px;
  overflow-x: auto;
  /* Permite desplazamiento horizontal si es necesario */
}

.table th,
.table td {
  padding: 8px;
  /* Asegura un espacio adecuado dentro de las celdas, sin afectar el tamaño */
  word-wrap: break-word;
  /* Permite que el texto largo se ajuste dentro de las celdas */
}

.table th {
  min-width: 150px;
  /* Establece un ancho mínimo para las cabeceras */
}

.table td {
  min-width: 150px;
  /* Establece un ancho mínimo para las celdas */
}

.card-header {
  padding: 10px 20px;
  background-color: #f7f7f7;
}

.card-body {
  padding: 20px;
  /* Relleno dentro de la tarjeta */
}

.sticky-col {
  position: sticky;
  left: 0;
  background-color: white;
  z-index: 2;
  /* Asegura que la columna se superponga sobre otras celdas */
}

.table th,
.table td {
  padding: 8px;
  word-wrap: break-word;
}

.table th {
  min-width: 150px;
}

.table td {
  min-width: 150px;
}

.active-page {
  background-color: #41b341;
  /* Verde más claro */
  color: white;
  /* Texto blanco */
  border-color: #41b341;
  /* Borde verde claro */
  font-weight: bold;
  /* Resalta un poco más el texto */
}

/* Sticky columns */
.sticky-col-0 {
  position: sticky;
  left: 0;
  background-color: white;
  z-index: 3;
  min-width: 70px;
  padding: 4px 6px;
}

.sticky-col-1 {
  position: sticky;
  left: 150px;
  background-color: white;
  z-index: 3;
  min-width: 70px;
  padding: 4px 6px;
}

.sticky-col-2 {
  position: sticky;
  left: 300px;
  background-color: white;
  z-index: 3;
  min-width: 70px;
  padding: 4px 6px;
}

.table th,
.table td {
  font-size: 0.8rem;
  /* de 1rem a 0.8rem */
  padding: 4px 6px;
  /* reduce el padding vertical y horizontal */
}
</style>