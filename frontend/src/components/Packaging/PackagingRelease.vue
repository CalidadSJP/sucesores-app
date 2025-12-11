<template>
    <div class="container mt-5">
        <!-- Tarjeta de formulario -->
        <div class="card mb-4">
            <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Liberación de Material de Empaque</h5>
                <div>
                    <!-- Botón para desplegar carpeta 
                    <button class="btn btn-outline-light btn-sm" @click="toggleDocuments">
                        <i class="fas fa-folder"></i> Fichas Técnicas
                    </button>-->
                </div>
            </div>
            <div class="card-body">
                <!-- Lista desplegable de PDFs
                <div v-if="showDocuments" class="mb-3">
                    <label class="form-label">Fichas Técnicas disponibles:</label>
                    <ul class="list-group">
                        <li v-for="doc in technicalSheets" :key="doc"
                            class="list-group-item d-flex justify-content-between align-items-center">
                            {{ doc }}
                            <button class="btn btn-sm btn-primary" @click="openModal(getPdfUrl(doc))">
                                <i class="fa-solid fa-eye"></i>
                            </button>
                        </li>
                    </ul>
                    <br> 
                </div>-->

                <form @submit.prevent="submitForm">
                    <div class="mb-3">
                        <label for="product" class="form-label">Lista de Productos (EN ESPERA)</label>
                        <select v-model="selectedProduct" id="product" class="form-select" required>
                            <option v-for="product in products" :key="product.id" :value="product.id">
                                {{ product.label }}
                            </option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">1) ¿Certificado de Análisis cumple con especificaciones? / ¿Concuerda
                            con análisis internos?</label>
                        <div>
                            <div class="form-check form-check-inline" v-for="option in ['SI', 'NO', 'NO APLICA']"
                                :key="option">
                                <input class="form-check-input" type="radio" :id="'analysis' + option" :value="option"
                                    v-model="analysisMatch" required />
                                <label class="form-check-label" :for="'analysis' + option">{{ option }}</label>
                            </div>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">2) ¿Cumple con los criterios de liberación?</label>
                        <div>
                            <div class="form-check form-check-inline" v-for="option in ['SI', 'NO']" :key="option">
                                <input class="form-check-input" type="radio" :id="'criteria' + option" :value="option"
                                    v-model="releaseCriteria" required />
                                <label class="form-check-label" :for="'criteria' + option">{{ option }}</label>
                            </div>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="releaser" class="form-label">Liberado por:</label>
                        <input type="text" id="releaser" v-model="releaser" @input="releaser = releaser.toUpperCase()"
                            class="form-control text-uppercase" required />
                    </div>

                    <button type="submit" class="btn btn-success">Registrar Liberación</button>
                </form>
            </div>
        </div>

        <!-- Modal para visualizar PDF 
        <div class="modal fade show" v-if="pdfModal" style="display: block; background: rgba(0,0,0,0.5);">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Ficha Técnica</h5>
                        <button type="button" class="btn-close" @click="pdfModal = false"></button>
                    </div>
                    <div class="modal-body">
                        <iframe :src="pdfToShow" style="width:100%; height:80vh; border:none;" allowfullscreen></iframe>
                    </div>
                </div>
            </div>
        </div>-->

        <!-- Tarjeta con tabla -->
        <div class="card">
            <div class="card-header bg-secondary text-white">
                <h5>Historial de Liberaciones</h5>
            </div>
            <div class="card-body p-0">
                <div class="scrollable-table">
                    <table class="table table-bordered table-hover align-middle">
                        <thead class="table-success text-center">
                            <tr>
                                <th>ID</th>
                                <th>Producto</th>
                                <th>Fecha</th>
                                <th>Cumple los criterios</th>
                                <th>Concuerda con los Análisis</th>
                                <th>Liberado?</th>
                                <th>Responsable</th>
                            </tr>
                        </thead>
                        <tbody class="text-center">
                            <tr v-for="entry in releases" :key="entry.id">
                                <td>{{ entry.id }}</td>
                                <td>{{ entry.product_name }}</td>
                                <td>{{ formatDate(entry.release_date) }}</td>
                                <td>{{ entry.release_criteria }}</td>
                                <td>{{ entry.analysis_match }}</td>
                                <td>{{ entry.release_status }}</td>
                                <td>{{ entry.releaser }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div v-if="releases.length === 0" class="text-center text-muted py-3">No hay registros todavía.</div>
            </div>
        </div><br><br>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            products: [],
            releases: [],
            selectedProduct: null,
            analysisMatch: "",
            releaseCriteria: "",
            releaser: "",
            showDocuments: false,
            technicalSheets: [],
            pdfModal: false,
            pdfToShow: ""
        };
    },
    methods: {
        toggleDocuments() {
            this.showDocuments = !this.showDocuments;
            if (this.showDocuments && this.technicalSheets.length === 0) {
                this.fetchTechnicalSheets();
            }
        },
        getPdfUrl(filename) {
            return `${process.env.VUE_APP_API_URL}/api/static/Fichas_Tecnicas/Aditivos/${filename}`;
        },
        async fetchProducts() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-pending-products`);
                this.products = response.data.map((product) => ({
                    id: product.id,
                    label: `${product.entry_date}_${product.product}_${product.supplier}`,
                }));
            } catch (error) {
                console.error("Error fetching products:", error);
            }
        },
        async fetchReleases() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-additive-releases`);
                this.releases = response.data;
            } catch (error) {
                console.error("Error fetching releases:", error);
            }
        },
        async fetchTechnicalSheets() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-technical-sheets`);
                this.technicalSheets = response.data.files;
            } catch (error) {
                console.error("Error fetching technical sheets:", error);
            }
        },
        async submitForm() {
            try {
                const status = this.analysisMatch === "SI" && this.releaseCriteria === "SI" ? "SI" : "NO";
                await axios.post(`${process.env.VUE_APP_API_URL}/api/submit-release`, {
                    product_id: this.selectedProduct,
                    analysis_match: this.analysisMatch,
                    release_criteria: this.releaseCriteria,
                    release_status: status,
                    releaser: this.releaser
                });
                alert("Liberación registrada exitosamente.");
                this.resetForm();
                this.fetchProducts();
                this.fetchReleases();
            } catch (error) {
                console.error("Error submitting release:", error);
                alert("Ocurrió un error al registrar la liberación.");
            }
        },
        resetForm() {
            this.selectedProduct = null;
            this.analysisMatch = "";
            this.releaseCriteria = "";
            this.releaser = "";
        },
        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleString("es-EC", {
                timeZone: "UTC",
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit"
            });
        },
        openModal(pdfUrl) {
            this.pdfToShow = pdfUrl;
            this.pdfModal = true;
        }
    },
    mounted() {
        this.fetchProducts();
        this.fetchReleases();
    }
};
</script>

<style>
.card {
    max-width: 1200px !important;
    margin: 0 auto 30px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.text-uppercase {
    text-transform: uppercase;
}

.scrollable-table {
    max-height: 300px;
    overflow-y: auto;
}

.scrollable-table thead th {
    position: sticky;
    top: 0;
    background-color: #d1e7dd;
    z-index: 1;
}
</style>
