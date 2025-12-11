<template>
    <div class="container mt-4">
        <div class="card shadow-sm modern-card">

            <!-- Header -->
            <div class="card-header d-flex justify-content-between align-items-center custom-header">
                <h4 class="mb-0 text-white">Movimientos de Limpieza</h4>

                <router-link to="/cleaning-home" class="btn btn-light btn-sm return-btn">
                    <i class="fas fa-arrow-left me-1"></i> Volver
                </router-link>
            </div>

            <div class="card-body">

                <!-- Tabla -->
                <div class="table-responsive">
                    <div class="table-wrapper">
<table class="table modern-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Producto</th>
                                <th>Fecha</th>
                                <th>Área</th>
                                <th>Ingreso</th>
                                <th>Egreso</th>
                                <th>Saldo</th>
                                <th>Observaciones</th>
                                <th>Responsable</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="row in paginatedData" :key="row.id">
                                <td>{{ row.id }}</td>
                                <td>{{ row.product_name }}</td>
                                <td>{{ formatDate(row.date) }}</td>
                                <td>{{ row.area }}</td>
                                <td>{{ row.income }}</td>
                                <td>{{ row.outcome }}</td>
                                <td>{{ row.balance }}</td>
                                <td>{{ row.observations }}</td>
                                <td>{{ row.responsible }}</td>
                            </tr>

                            <tr v-if="paginatedData.length === 0">
                                <td colspan="9" class="text-center py-3">No hay movimientos disponibles.</td>
                            </tr>
                        </tbody>

                    </table>
</div>
                </div>

                <!-- Paginación -->
                <nav class="mt-4">
                    <ul class="pagination justify-content-center">

                        <li class="page-item" :class="{ disabled: currentPage === 1 }">
                            <a class="page-link pagination-btn" href="#" @click.prevent="changePage(currentPage - 1)">
                                &laquo;
                            </a>
                        </li>

                        <li v-for="page in visiblePages" :key="page"
                            class="page-item"
                            :class="{ active: currentPage === page }">

                            <a class="page-link pagination-number" href="#"
                                @click.prevent="changePage(page)">
                                {{ page }}
                            </a>
                        </li>

                        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                            <a class="page-link pagination-btn" href="#" @click.prevent="changePage(currentPage + 1)">
                                &raquo;
                            </a>
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
            allData: [],
            currentPage: 1,
            pageSize: 15,
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.allData.length / this.pageSize);
        },
        paginatedData() {
            const start = (this.currentPage - 1) * this.pageSize;
            return this.allData.slice(start, start + this.pageSize);
        },
        visiblePages() {
            const maxPagesToShow = 5;
            const pages = [];

            let start = Math.max(1, this.currentPage - Math.floor(maxPagesToShow / 2));
            let end = start + maxPagesToShow - 1;

            if (end > this.totalPages) {
                end = this.totalPages;
                start = Math.max(1, end - maxPagesToShow + 1);
            }

            for (let i = start; i <= end; i++) {
                pages.push(i);
            }

            return pages;
        },
    },
    methods: {
        async fetchData() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/cleaning-movements`);
                if (Array.isArray(response.data)) {
                    this.allData = response.data;
                }
            } catch (error) {
                console.error('Error al cargar movimientos:', error);
            }
        },
        changePage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },
        formatDate(dateStr) {
            if (!dateStr) return 'Fecha inválida';

            const onlyDate = dateStr.split('T')[0];
            const [year, month, day] = onlyDate.split('-');
            return `${day}/${month}/${year}`;
        }

    },
    mounted() {
        this.fetchData();
    },
};
</script>

<style scoped>
/* CARD MÁS LIMPIA */
.modern-card {
    border-radius: 12px;
    overflow: hidden;
}

/* HEADER VERDE ELEGANTE */
.custom-header {
    background: #019c54;
    padding: 1rem 1.2rem;
}

/* BOTÓN VOLVER */
.return-btn {
    border-radius: 50px;
    font-weight: 500;
    transition: background 0.2s ease;
}

.return-btn:hover {
    background: #e7f7ed;
}

/* TABLA PROFESIONAL */
.table {
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.9rem;
}

.table thead th {
    background: #f8f9fa;
    font-weight: 600;
    border-bottom: 2px solid #dee2e6;
}

.table tbody tr {
    border-bottom: 1px solid #e5e5e5;
}

.table-hover tbody tr:hover {
    background-color: #f3f7ff !important;
}

.table td,
.table th {
    border-right: 1px solid #e6e6e6;
}

.table td:last-child,
.table th:last-child {
    border-right: none;
}

/* PAGINACIÓN MODERNA */
.pagination-number,
.pagination-btn {
    border-radius: 50px !important;
    margin: 0 4px;
    padding: 8px 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    transition: all 0.2s ease;
    border: none !important;
    background: #ffffff;
    color: #198754;
    font-weight: 500;
}

.pagination-number:hover,
.pagination-btn:hover {
    background: #198754;
    color: white;
    box-shadow: 0 3px 10px rgba(25, 135, 84, 0.35);
}

/* ACTIVA */
.page-item.active .page-link {
    background: #198754 !important;
    color: white !important;
    font-weight: bold;
    box-shadow: 0 0 8px rgba(25, 135, 84, 0.5);
}

/* DESHABILITADA */
.page-item.disabled .page-link {
    opacity: 0.4;
    pointer-events: none;
}
.table-wrapper {
  max-height: 400px;
  overflow-y: auto;
}
</style>
