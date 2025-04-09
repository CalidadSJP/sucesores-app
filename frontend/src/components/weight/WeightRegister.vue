<template>
    <div class="container-fluid mt-4">
        <h2 class="text-center">Registro de Pesos</h2><br>

        <!-- Tarjeta con tabla y mayor ancho -->
        <div class="card shadow-lg mx-auto" style="max-width: 90%; width: 100%;">
            <!-- Header de la tarjeta con el filtro -->
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Filtrar Registro</h5>
                <div class="d-flex align-items-center">
                    <input v-model="startDate" type="date" class="form-control me-2" placeholder="Fecha inicio">
                    <input v-model="endDate" type="date" class="form-control me-2" placeholder="Fecha fin">

                </div>
            </div>

            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped table-bordered">
                        <thead class="table-dark">
                            <tr>
                                <th v-for="(column, index) in columns" :key="index">
                                    {{ column.label }}
                                </th>
                                <th>Acciones</th>
                            </tr>
                            <tr>
                                <th v-for="(column, index) in columns" :key="'filter-' + index">
                                    <!-- Filtro por columna -->
                                    <input v-if="column.filterable" v-model="filters[column.key]" class="form-control"
                                        :placeholder='"Filtrar..."' />
                                </th>
                                <th></th> <!-- Para la columna de Acciones -->
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="row in paginatedData" :key="row.id">
                                <td v-for="(column, colIndex) in columns" :key="colIndex">
                                    <input v-if="editMode[row.id]" v-model="row[column.key]" class="form-control">
                                    <span v-else>{{ row[column.key] }}</span>
                                </td>
                                <td>
                                    <button v-if="!editMode[row.id]" class="btn btn-warning btn-sm"
                                        @click="enableEdit(row.id)">Editar</button>
                                    <button v-else class="btn btn-success btn-sm"
                                        @click="saveEdit(row)">Guardar</button>
                                    <button v-if="editMode[row.id]" class="btn btn-danger btn-sm ms-2 mr-2"
                                        @click="cancelEdit(row.id)">Cancelar</button>

                                    <button class="btn btn-danger btn-sm ms-2 mt-2"
                                        @click="confirmDelete(row.id)">Eliminar</button>
                                </td>

                            </tr>
                        </tbody>
                    </table>
                </div><br>

                <div class="d-flex justify-content-between mb-3">
                    <button @click="downloadExcel" class="btn btn-success">Descargar Registro</button>
                    <button @click="clearFilters" class="btn btn-secondary px-3">Limpiar Filtros</button>
                </div>

                <br>
                <!-- Paginación -->
                <nav>
                    <ul class="pagination justify-content-center">
                        <li class="page-item" :class="{ disabled: currentPage === 1 }">
                            <button class="page-link" @click="goToPage(currentPage - 1)">Anterior</button>
                        </li>

                        <!-- Paginación de 5 páginas a la vez -->
                        <li class="page-item" :class="{ disabled: currentPage === page }" v-for="page in paginatedPages"
                            :key="page">
                            <button class="page-link" @click="goToPage(page)">{{ page }}</button>
                        </li>

                        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                            <button class="page-link" @click="goToPage(currentPage + 1)">Siguiente</button>
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
            records: [],
            startDate: "",
            endDate: "",
            filters: {
                date: "",
                baler: "",
                ean13: "",
                net_weight: "",
                format: "",
                brand: "",
                lot: "",
                manufacture_date: "",
                expiry_date: "",
                average: "",
                minimum: "",
                maximum: "",
                standard_deviation: "",
                result: "",
                count_t1: "",
                count_t2: "",
                percent_t1: "",
                limite_maximo_operativo: "",
                limite_minimo_operativo: ""
            },
            columns: [
                { key: "id", label: "ID" },
                { key: "date", label: "Fecha", filterable: false },
                { key: "baler", label: "Empacadora", filterable: true },
                { key: "ean13", label: "EAN 13", filterable: true },
                { key: "net_weight", label: "Peso Neto", filterable: true },
                { key: "format", label: "Formato", filterable: true },
                { key: "brand", label: "Marca", filterable: true },
                { key: "lot", label: "Lote", filterable: true },
                { key: "manufacture_date", label: "Fecha de Fabricación", filterable: false },
                { key: "expiry_date", label: "Fecha de Expiración", filterable: false },
                { key: "average", label: "Peso Promedio", filterable: false },
                { key: "minimum", label: "Peso Mínimo", filterable: false },
                { key: "maximum", label: "Peso Máximo", filterable: false },
                { key: "standard_deviation", label: "Desviación Estándar", filterable: false },
                { key: "result", label: "Resultado", filterable: false },
                { key: "count_t1", label: "Errores T1", filterable: false },
                { key: "count_t2", label: "Errores T2", filterable: false },
                { key: "percent_t1", label: "% T1", filterable: false },
                { key: "limite_maximo_operativo", label: "Límite Máximo", filterable: false },
                { key: "limite_minimo_operativo", label: "Límite Mínimo", filterable: false },
                ...Array.from({ length: 30 }, (_, i) => ({ key: `p${i + 1}`, label: `P${i + 1}`, filterable: false }))
            ],
            currentPage: 1,
            itemsPerPage: 10,
            editMode: {},
            originalData: {}
        };
    },
    computed: {
        filteredData() {
            return this.records
                .filter(row => {
                    // Filtrado de fechas
                    const rowDate = row.date ? this.parseDate(row.date) : null;
                    const start = this.startDate ? new Date(this.startDate) : null;
                    const end = this.endDate ? new Date(this.endDate) : null;

                    const isValidDate = rowDate instanceof Date && !isNaN(rowDate);
                    const isDateFiltered = this.startDate || this.endDate;
                    const matchesDate = !isDateFiltered || (
                        isValidDate &&
                        (!start || rowDate >= start) &&
                        (!end || rowDate <= end)
                    );

                    // Filtrar por cada columna
                    const matchesFilters = Object.keys(this.filters).every(key => {
                        const filterValue = this.filters[key];
                        const rowValue = row[key];
                        return !filterValue || String(rowValue).toLowerCase().includes(filterValue.toLowerCase());
                    });

                    return matchesDate && matchesFilters;
                })
                .sort((a, b) => b.id - a.id); // Ordenar por ID de forma ascendente
        },

        totalPages() {
            return Math.ceil(this.filteredData.length / this.itemsPerPage);
        },
        paginatedData() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            return this.filteredData.slice(start, start + this.itemsPerPage);
        },
        paginatedPages() {
            const totalPages = this.totalPages;
            const pageGroup = Math.floor((this.currentPage - 1) / 5) * 5;
            const pages = [];
            for (let i = pageGroup + 1; i <= pageGroup + 5 && i <= totalPages; i++) {
                pages.push(i);
            }
            return pages;
        }
    },
    methods: {
        clearFilters() {
            this.startDate = "";
            this.endDate = "";
            Object.keys(this.filters).forEach(key => {
                this.filters[key] = "";
            });
        },
        parseDate(dateStr) {
            const [day, month, year] = dateStr.split('-');
            return new Date(`${year}-${month}-${day}`);
        },
        async fetchData() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/weight-control`);
                this.records = response.data;
            } catch (error) {
                console.error("Error obteniendo los datos:", error);
            }
        },
        formatLabel(key) {
            const labels = {
                id: "ID", date: "Fecha", baler: "Empacadora", net_weight: "Peso Neto",
                format: "Formato", brand: "Marca", lot: "Lote", manufacture_date: "Fecha de Fabricación",
                expiry_date: "Fecha de Expiración", average: "Peso Promedio", minimum: "Peso Mínimo",
                maximum: "Peso Máximo", standard_deviation: "Desviación Estándar", result: "Resultado",
                count_t1: "Errores T1", count_t2: "Errores T2", percent_t1: "% T1",
                limite_maximo_operativo: "Límite Máximo", limite_minimo_operativo: "Límite Mínimo", ean13: "EAN 13"
            };
            return labels[key] || key;
        },
        enableEdit(id) {
            this.editMode[id] = true;
            this.originalData[id] = { ...this.records.find(row => row.id === id) };
        },
        async saveEdit(row) {
            try {
                await axios.put(`${process.env.VUE_APP_API_URL}/api/weight-control/${row.id}`, row);
                this.editMode[row.id] = false;
                console.log("Registro actualizado con éxito.");
            } catch (error) {
                console.error("Error al actualizar el registro:", error);
            }
        },
        cancelEdit(id) {
            const index = this.records.findIndex(row => row.id === id);
            this.records[index] = { ...this.originalData[id] };
            this.editMode[id] = false;
        },
        goToPage(page) {
            if (page < 1 || page > this.totalPages) return;
            this.currentPage = page;
        },
        async downloadExcel() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/download-weight-control`, {
                    responseType: 'blob'
                });

                // Validar tipo MIME recibido
                const contentType = response.headers['content-type'];
                if (!contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')) {
                    console.error("Tipo de archivo inesperado:", contentType);
                    const errorText = await response.data.text(); // si viene como texto (por ejemplo JSON de error)
                    throw new Error("Respuesta inesperada del servidor: " + errorText);
                }

                const blob = new Blob([response.data], { type: contentType });
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'registro_pesos.xlsx');
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
            } catch (error) {
                console.error("Error al descargar el archivo:", error);
            }
        },
        confirmDelete(id) {
            if (confirm("¿Estás seguro de que deseas eliminar este registro? Esta acción no se puede deshacer.")) {
                this.deleteRecord(id);
            }
        },
        async deleteRecord(id) {
            try {
                await axios.delete(`${process.env.VUE_APP_API_URL}/api/weight-control/${id}`);
                this.records = this.records.filter(record => record.id !== id);
                alert("Registro eliminado con éxito.");
            } catch (error) {
                console.error("Error al eliminar el registro:", error);
                alert("Ocurrió un error al eliminar el registro.");
            }
        },


    },
    mounted() {
        this.fetchData();
    }
};
</script>


<style scoped>
.card {
    border-radius: 10px;
    max-width: 100%;
    width: 100%;
}

.container-fluid {
    max-width: 100%;
}

.table th,
.table td {
    text-align: center;
    vertical-align: middle;
    width: 150px;
}

.table th {
    min-width: 100px;
}

.btn {
    min-width: 100px;
}

/* Estilos adicionales para el encabezado de la tarjeta */
.card-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid #ddd;
    font-size: 18px;
    font-weight: bold;
}

.card-header .form-control {
    width: 50%;
}

.btn-success {
    margin-left: 10px;
    /* Agrega espacio a la derecha del botón de guardar */
    margin-right: 10px;
}

/* Añadir margen al botón de cancelar */
.btn-danger {
    margin-top: 10px;
    /* Agrega espacio a la izquierda del botón de cancelar */
    margin-right: 10px
}
</style>