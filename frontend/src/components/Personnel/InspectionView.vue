<template>
    <div class="container-fluid p-4">
        <h1 class="text-center mb-4">Registro - Control de Prácticas de Personal</h1>
        <div class="card">
            <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                <h4>Tabla Editable</h4>
                <div>
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
                    <table class="table table-bordered table-striped"
                        style="table-layout: auto; font-size: 0.8rem; border-collapse: collapse; width: 100%;">

                        <thead>
                            <tr>
                                <th v-for="(header, index) in headers" :key="header"
                                    :class="{ 'sticky-col': index === 0 }">
                                    {{ header }}
                                </th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(row, index) in paginatedData" :key="row.id">
                                <td v-for="(key, colIndex) in keys" :key="key"
                                    :class="{ 'sticky-col': colIndex === 0 }">
                                    <input v-if="editableRow === index" :value="row[key]"
                                        @input="row[key] = $event.target.value.toUpperCase()" class="form-control"
                                        type="text" />
                                    <span v-else>{{ row[key] }}</span>
                                </td>
                                <td>
                                    <button v-if="editableRow === index" class="btn btn-success btn-sm ms-1"
                                        @click="saveRow(index)">
                                        Guardar
                                    </button>
                                    <button v-else class="btn btn-info btn-sm mb-1 mt-1 ms-1" @click="editRow(index)">
                                        Editar
                                    </button>
                                    <button class="btn btn-danger btn-sm mt-1 mb-1 ms-1" @click="deleteRow(row.id)">
                                        Eliminar
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Paginación -->
                <nav aria-label="Paginación" class="d-flex justify-content-center mt-4">
                    <ul class="pagination">
                        <!-- Botón Anterior -->
                        <li class="page-item" :class="{ disabled: currentPage === 1 }">
                            <button class="page-link bg-success text-white border-success" @click="previousPage">
                                Anterior
                            </button>
                        </li>

                        <!-- Botones de Páginas -->
                        <li class="page-item" v-for="page in visiblePages" :key="page"
                            :class="{ active: currentPage === page }">
                            <button class="page-link" @click="currentPage = page"
                                :class="currentPage === page ? 'active-page' : 'bg-success text-white border-success'">
                                {{ page }}
                            </button>
                        </li>

                        <!-- Botón Siguiente -->
                        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                            <button class="page-link bg-success text-white border-success" @click="nextPage">
                                Siguiente
                            </button>
                        </li>
                    </ul>
                </nav>
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
                "Fecha",
                "Turno",
                "Área",
                "Nombre del operario",
                "Manos limpias",
                "Uniforme limpio",
                "No objetos personales",
                "Heridas protegidas",
                "Cofia bien puesta",
                "Mascarilla bien colocada",
                "Uso de protector auditivo",
                "Uñas cortas",
                "Guantes limpios",
                "Pestañas",
                "Barba/Bigote",
                "Medicamento autorizado",
                "Supervisor",
                "Observaciones"
            ],
            keys: [
                "fecha",
                "turno",
                "area",
                "nombre_operario",
                "manos_limpias",
                "uniforme_limpio",
                "no_objetos_personales",
                "heridas_protegidas",
                "cofia_bien_puesta",
                "mascarilla_bien_colocada",
                "protector_auditivo",
                "unas_cortas",
                "guantes_limpios",
                "pestanas",
                "barba_bigote",
                "medicamento_autorizado",
                "supervisor",
                "observaciones"
            ],
            tableData: [],        // Datos completos
            editableRow: null,
            searchQuery: "",      // Consulta de búsqueda
            currentPage: 1,       // Página actual
            itemsPerPage: 5,     // Elementos por página
            pagesPerGroup: 5
        };
    },
    computed: {

        totalPages() {
            return Math.ceil(this.filteredData.length / this.itemsPerPage);
        },
        visiblePages() {
            const start = Math.floor((this.currentPage - 1) / this.pagesPerGroup) * this.pagesPerGroup + 1;
            const end = Math.min(start + this.pagesPerGroup - 1, this.totalPages);

            const pages = [];
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            return pages;
        },
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
        paginatedData() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.filteredData.slice(start, end);
        },

    },
    methods: {
        fetchTableData() {
            axios
                .get(`${process.env.VUE_APP_API_URL}/api/inspection-register`)
                .then((response) => {
                    this.tableData = response.data;

                    // Formatear las fechas en el formato yyyy-mm-dd para su visualización en la tabla
                    this.tableData.forEach((row) => {
                        if (row.fecha) {
                            row.fecha = this.formatDate(row.fecha);
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
                .put(`${process.env.VUE_APP_API_URL}/api/inspection-register/${updatedRow.id}`, updatedRow)
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
                    .delete(`${process.env.VUE_APP_API_URL}/api/inspection-register/${id}`)
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
                url: `${process.env.VUE_APP_API_URL}/api/download-material-table`,
                method: 'GET',
                responseType: 'blob', // Importante para manejar archivos binarios
            })
                .then((response) => {
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', 'registro-material-empaque.xlsx');
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                })
                .catch((error) => {
                    console.error("Error al descargar el archivo:", error);
                    alert("Ocurrió un error al intentar descargar el archivo.");
                });
        },
        logout() {
            // Limpia el almacenamiento local y redirige al usuario
            localStorage.removeItem('authToken'); // Elimina el token
            localStorage.removeItem('user_area'); // Elimina el área
            localStorage.removeItem('user_id'); // Elimina el ID del usuario
            this.$router.push('/login-inspection-view'); // Redirige al login
        },
        previousPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
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
    margin: 5px;
    /* Espacio alrededor de la tarjeta */
    padding: 5px;
    /* Relleno dentro de la tarjeta */
    max-width: 1440px;
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
    min-width: 80px;
}

.table td {
    min-width: 90px;
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
</style>