<template>
    <div class="container mt-5">
      <div class="card">
        <div class="card-header bg-success text-white">
          <h5>Liberación de Aditivos</h5>
        </div>
        <div class="card-body">
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
              <label class="form-label">1) Concuerda con análisis internos?</label>
              <div>
                <div class="form-check form-check-inline">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="analysis"
                    id="analysisYes"
                    value="SI"
                    v-model="analysisMatch"
                    required
                  />
                  <label class="form-check-label" for="analysisYes">Sí</label>
                </div>
                <div class="form-check form-check-inline">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="analysis"
                    id="analysisNo"
                    value="NO"
                    v-model="analysisMatch"
                  />
                  <label class="form-check-label" for="analysisNo">No</label>
                </div>
              </div>
            </div>
  
            <div class="mb-3">
              <label class="form-label">2) Cumple con los criterios de liberación?</label>
              <div>
                <div class="form-check form-check-inline">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="releaseCriteria"
                    id="criteriaYes"
                    value="SI"
                    v-model="releaseCriteria"
                    required
                  />
                  <label class="form-check-label" for="criteriaYes">Sí</label>
                </div>
                <div class="form-check form-check-inline">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="releaseCriteria"
                    id="criteriaNo"
                    value="NO"
                    v-model="releaseCriteria"
                  />
                  <label class="form-check-label" for="criteriaNo">No</label>
                </div>
              </div>
            </div>
  
            <button type="submit" class="btn btn-success">Registrar Liberación</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        products: [],
        selectedProduct: null,
        analysisMatch: "",
        releaseCriteria: "",
      };
    },
    methods: {
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
      async submitForm() {
        try {
          const status = this.analysisMatch === "YES" && this.releaseCriteria === "YES" ? "YES" : "NO";
          await axios.post(`${process.env.VUE_APP_API_URL}/api/submit-release`, {
            product_id: this.selectedProduct,
            analysis_match: this.analysisMatch,
            release_criteria: this.releaseCriteria,
            release_status: status,
          });
          alert("Liberación registrada exitosamente.");
          this.resetForm();
          this.fetchProducts(); // Refresca la lista
        } catch (error) {
          console.error("Error submitting release:", error);
          alert("Ocurrió un error al registrar la liberación.");
        }
      },
      resetForm() {
        this.selectedProduct = null;
        this.analysisMatch = "";
        this.releaseCriteria = "";
      },
    },
    mounted() {
      this.fetchProducts();
    },
  };
  </script>
  
  <style>
  .card {
    max-width: 600px;
    margin: 0 auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  </style>
  