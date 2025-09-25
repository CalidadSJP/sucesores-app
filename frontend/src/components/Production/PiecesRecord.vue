<template>
    <div class="container mt-5">
        <h2 class="mb-4 text-center">Registros de Inspecciones</h2>

        <!-- Filtros -->
        <div class="card p-3 mb-4 shadow-sm">
            <div class="row">
                <div class="col-md-4">
                    <label for="filterLine">Línea de Producción</label>
                    <select v-model="filters.line_id" @change="fetchInspections" class="form-control">
                        <option value="">Todas</option>
                        <option v-for="line in productionLines" :key="line.id" :value="line.id">
                            {{ line.line_name }}
                        </option>
                    </select>
                </div>

                <div class="col-md-4">
                    <label for="filterPiece">Elemento</label>
                    <input type="text" v-model="filters.piece" @input="fetchInspections" class="form-control"
                        placeholder="Buscar por elemento" />
                </div>

                <div class="col-md-4">
                    <label for="filterDate">Fecha</label>
                    <input type="date" v-model="filters.date" @change="fetchInspections" class="form-control" />
                </div>
            </div>
        </div>

        <!-- Tabla de Registros -->

        <div class="card shadow-sm">
            <div class="table-responsive">
                <table class="table table-striped table-hover text-center align-middle">
                    <thead class="table-dark">
                        <tr>
                            <th rowspan="2">Fecha</th>
                            <th rowspan="2">Línea</th>
                            <th rowspan="2" class="section-border-right">Elemento</th>
                            <th colspan="3" class="section-border-left section-border-right">Revisión de Bulbo</th>
                            <th colspan="3" class="section-border-left section-border-right">Revisión del Conector de
                                Alimentación</th>
                            <th colspan="2" class="section-border-left section-border-right">Revisión del Conector Sonda
                            </th>
                            <th rowspan="2" class="section-border-left">Observaciones</th>
                        </tr>
                        <tr>
                            <!-- Revisión de Bulbo -->
                            <th class="section-border-left">Malla</th>
                            <th>Tornillo</th>
                            <th class="section-border-right">Plástico</th>
                            <!-- Revisión Conector Alimentación -->
                            <th class="section-border-left">Sujeción</th>
                            <th>Ajuste (Tuerca)</th>
                            <th class="section-border-right">Plástico</th>
                            <!-- Revisión Conector Sonda -->
                            <th class="section-border-left">Ajuste al Transductor</th>
                            <th class="section-border-right">Plástico</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="record in inspections" :key="record.id">
                            <td>{{ formatDate(record.inspection_date) }}</td>
                            <td>{{ record.line_name }}</td>
                            <td class="section-border-right">{{ record.piece }}</td>
                            <td class="section-border-left">{{ record.mesh }}</td>
                            <td>{{ record.screw }}</td>
                            <td class="section-border-right">{{ record.bulb_plastic }}</td>
                            <td class="section-border-left">{{ record.connector_mounting }}</td>
                            <td>{{ record.connector_adjustment }}</td>
                            <td class="section-border-right">{{ record.connector_plastic }}</td>
                            <td class="section-border-left">{{ record.transducer_adjustment }}</td>
                            <td class="section-border-right">{{ record.probe_plastic }}</td>
                            <td class="section-border-left">{{ record.observations }}</td>
                        </tr>
                        <tr v-if="inspections.length === 0">
                            <td colspan="12" class="text-center">No hay registros encontrados</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <!-- Paginación -->
            <div v-if="totalPages > 1" class="pagination-container text-center mt-4">
                <button v-if="currentPage > 10" class="pagination-btn" @click="changePage(currentPage - 10)">
                    « -10
                </button>

                <button v-if="currentPage > 1" class="pagination-btn" @click="changePage(currentPage - 1)">
                    «
                </button>

                <button v-for="page in visiblePages" :key="page" class="pagination-btn"
                    :class="{ active: page === currentPage }" @click="changePage(page)">
                    {{ page }}
                </button>

                <button v-if="currentPage < totalPages" class="pagination-btn" @click="changePage(currentPage + 1)">
                    »
                </button>

                <button v-if="currentPage + 10 <= totalPages" class="pagination-btn"
                    @click="changePage(currentPage + 10)">
                    +10 »
                </button>
            </div><br>

            <div class="card-footer text-end">
                <button class="btn btn-primary me-2" @click="$router.push('/pieces-inspection')">
                    <i class="fas fa-arrow-left"></i> Volver
                </button>
                <button class="btn btn-success" @click="downloadExcel">
                    <i class="fas fa-file-excel"></i> Descargar Excel
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            productionLines: [],
            inspections: [],
            allInspections: [], // todos los registros,
            filters: {
                line_id: '',
                piece: '',
                date: ''
            },
            // Variables para la paginación
            currentPage: 1,
            pageSize: 10, // registros por página
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.allInspections.length / this.pageSize);
        },
        visiblePages() {
            const total = this.totalPages;
            let start = Math.max(1, this.currentPage - 2);
            let end = Math.min(total, start + 4);
            if (end - start < 4) {
                start = Math.max(1, end - 4);
            }
            let pages = [];
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            return pages;
        }
    },
    created() {
        this.fetchLines();
        this.fetchInspections();
    },
    methods: {
        formatDate(dateString) {
            const date = new Date(dateString);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
        async fetchLines() {
            try {
                const res = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-lines`);
                this.productionLines = res.data;
            } catch (error) {
                console.error('Error al cargar líneas:', error);
            }
        },
        async fetchInspections() {
            try {
                const cleanFilters = {};
                if (this.filters.line_id) cleanFilters.line_id = this.filters.line_id;
                if (this.filters.piece.trim()) cleanFilters.piece = this.filters.piece.trim();
                if (this.filters.date) cleanFilters.date = this.filters.date;

                const res = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-piece-inspections`, {
                    params: cleanFilters
                });

                this.allInspections = res.data;
                this.setPage(1); // mostrar primera página
            } catch (error) {
                console.error('Error al obtener inspecciones:', error);
            }
        },
        changePage(page) {
            this.setPage(page);
        },
        setPage(page) {
            if (page < 1 || page > this.totalPages) return;
            this.currentPage = page;
            const start = (page - 1) * this.pageSize;
            const end = start + this.pageSize;
            this.inspections = this.allInspections.slice(start, end);
        },
        downloadExcel() {
            const query = new URLSearchParams(this.filters).toString();
            const url = `${process.env.VUE_APP_API_URL}/api/download-piece-inspections?${query}`;
            window.open(url, '_blank');
        }
    }
};
</script>

<style scoped>
.table {
    font-size: 0.95rem;
}

.card-footer {
    background: #f8f9fa;
}

.table th,
.table td {
    border: 1px solid #dee2e6 !important;
    /* Forzar bordes internos */
}

.section-border-right {
    border-right: 3px solid #343a40 !important;
    /* Línea gruesa para separar secciones */
}

.section-border-left {
    border-left: 3px solid #343a40 !important;
}

/* Estilos para la paginación */
.pagination-container {
    display: flex;
    justify-content: center;
    gap: 6px;
    flex-wrap: wrap;
}

.pagination-btn {
    background-color: #28a745;
    border: 2px solid #218838;
    color: white;
    border-radius: 50%;
    width: 38px;
    height: 38px;
    text-align: center;
    font-weight: bold;
    cursor: pointer;
    transition: 0.2s;
}

.pagination-btn:hover {
    background-color: #218838;
}

.pagination-btn.active {
    background-color: white;
    color: #28a745;
    border-color: #28a745;
}
</style>
