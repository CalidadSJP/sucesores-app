<template>
    <div class="container mt-5">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0">Movimientos de Limpieza</h4>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-bordered table-hover">
                        <thead class="table-light">
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
                                <td colspan="8" class="text-center">No hay movimientos disponibles.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Paginación -->
                <nav class="mt-3">
                    <ul class="pagination justify-content-center">
                        <li class="page-item" :class="{ disabled: currentPage === 1 }">
                            <a class="page-link rounded-pill nav-arrow" href="#"
                                @click.prevent="changePage(currentPage - 1)">
                                &laquo;
                            </a>
                        </li>

                        <li v-for="page in visiblePages" :key="page" class="page-item"
                            :class="{ active: currentPage === page }">
                            <a class="page-link rounded-circle page-number" href="#" @click.prevent="changePage(page)">
                                {{ page }}
                            </a>
                        </li>

                        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                            <a class="page-link rounded-pill nav-arrow" href="#"
                                @click.prevent="changePage(currentPage + 1)">
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
.card {
    max-height: 80vh;
    overflow: auto;
}

.table th,
.table td {
    vertical-align: middle;
}
</style>
