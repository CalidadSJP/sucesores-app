<template>
    <div class="container mt-3">

        <!-- Tarjeta contenedora completa -->
        <div class="card main-card shadow-lg">

            <!-- Header dentro de la tarjeta -->
            <div class="card-header d-flex justify-content-between align-items-center page-header">

                <!-- Título a la izquierda -->
                <h2 class="m-0 fw-bold text-white">
                    Listado de Productos
                </h2>

                <!-- Botón Home a la derecha -->
                <button class="btn btn-light btn-sm home-btn" @click="$router.push('/cleaning-home')">
                    <i class="fas fa-arrow-left me-2"></i>Regresar
                </button>
            </div>



            <!-- Contenido principal -->
            <div class="card-body p-4">
                <div class="row g-4">

                    <!-- LISTADO -->
                    <div class="col-md-7">
                        <div class="card sub-card shadow-sm p-3 h-100">

                            <!-- Filtros -->
                            <div class="row g-2 mb-3">
                                <div class="col-md-6">
                                    <select class="form-select" v-model="filterType">
                                        <option value="">Tipo...</option>
                                        <option value="PAPEL">PAPEL</option>
                                        <option value="INSECTICIDAS">INSECTICIDAS</option>
                                        <option value="JABONES Y DESINFECTANTES">JABONES Y DESINFECTANTES</option>
                                        <option value="ESCOBAS Y TRAPEADORES">ESCOBAS Y TRAPEADORES</option>
                                        <option value="CEPILLOS ESPECIALES">CEPILLOS ESPECIALES</option>
                                    </select>
                                </div>

                                <div class="col-md-6">
                                    <input type="text" class="form-control" v-model="searchTerm"
                                        placeholder="Buscar producto..." />
                                </div>
                            </div>

                            <!-- Lista -->
                            <div class="scrollable-list">
                                <ul class="list-group">
                                    <li v-for="product in filteredProducts" :key="product.id"
                                        class="list-group-item d-flex justify-content-between align-items-center">

                                        <div class="product-info">
                                            <strong>{{ product.name }}</strong><br>
                                            <small class="text-muted">Cantidad: {{ product.quantity }}</small><br>
                                            <small class="text-muted">Tipo: {{ product.type }}</small><br>
                                            <small class="text-muted">Stock min: {{ product.minimum }}</small>

                                            <!-- Alertas -->
                                            <div v-if="product.quantity <= product.minimum"
                                                class="text-danger fw-bold mt-1">
                                                ⚠ Stock crítico ({{ product.quantity }})
                                            </div>
                                            <div v-else-if="product.quantity <= product.minimum + 2"
                                                class="text-warning fw-bold mt-1">
                                                ⚠ Stock bajo ({{ product.quantity }})
                                            </div>
                                        </div>

                                        <div class="btn-group">
                                            <button class="btn btn-sm btn-outline-primary"
                                                @click="selectProduct(product)">
                                                <i class="fas fa-edit"></i>
                                            </button>
                                            <button class="btn btn-sm btn-outline-danger"
                                                @click="deleteProduct(product.id)">
                                                <i class="fas fa-trash-alt"></i>
                                            </button>
                                        </div>
                                    </li>
                                </ul>
                            </div>

                        </div>
                    </div>

                    <!-- FORMULARIO -->
                    <div class="col-md-5">
                        <div class="card sub-card shadow-sm p-4">
                            <h5 class="card-title mb-3 text-center fw-bold">
                                {{ editingProductId ? 'Editar Producto' : 'Nuevo Producto' }}
                            </h5>

                            <form @submit.prevent="submitForm">
                                <div class="mb-3">
                                    <label class="form-label">Nombre del Producto</label>
                                    <input type="text" class="form-control text-uppercase" v-model="productName"
                                        required>
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Cantidad Inicial</label>
                                    <input type="number" class="form-control" v-model="initialQuantity" required
                                        min="0">
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Tipo</label>
                                    <select class="form-select" v-model="productType" required>
                                        <option disabled value="">Selecciona un tipo</option>
                                        <option value="PAPEL">PAPEL</option>
                                        <option value="INSECTICIDAS">INSECTICIDAS</option>
                                        <option value="JABONES Y DESINFECTANTES">JABONES Y DESINFECTANTES</option>
                                        <option value="ESCOBAS Y TRAPEADORES">ESCOBAS Y TRAPEADORES</option>
                                        <option value="CEPILLOS ESPECIALES">CEPILLOS ESPECIALES</option>
                                    </select>
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Stock Mínimo</label>
                                    <input type="number" class="form-control" v-model="minimumStock" required min="0">
                                </div>

                                <button type="submit" class="btn btn-success w-100">
                                    <i class="fas fa-save"></i>
                                    {{ editingProductId ? 'Actualizar' : 'Agregar' }}
                                </button>

                                <button v-if="editingProductId" class="btn btn-secondary w-100 mt-2" @click="resetForm">
                                    Cancelar Edición
                                </button>
                            </form>

                        </div>
                    </div>

                </div>
            </div>

        </div>

    </div><br>
</template>



<script>
import axios from 'axios';

export default {
    data() {
        return {
            products: [],
            productName: '',
            initialQuantity: 0,
            productType: '',
            minimumStock: 0,
            editingProductId: null,
            searchTerm: '',  // 🔍 <-- Nueva variable
            filterType: '', // 👈 NUEVO FILTRO DE TIPO
        };
    },
    created() {
        this.fetchProducts();
    },
    computed: {
        filteredProducts() {
            const term = this.searchTerm.toLowerCase();
            return this.products.filter(product => {
                const matchesSearch = product.name.toLowerCase().includes(term) || product.type.toLowerCase().includes(term);
                const matchesType = this.filterType === '' || product.type === this.filterType;
                return matchesSearch && matchesType;
            });
        }
    },

    methods: {
        selectProduct(product) {
            this.editingProductId = product.id;
            this.productName = product.name;
            this.initialQuantity = product.quantity;
            this.productType = product.type;
            this.minimumStock = product.minimum;
        },
        async fetchProducts() {
            try {
                const res = await axios.get(`${process.env.VUE_APP_API_URL}/api/cleaning-products-list`);
                this.products = res.data;
            } catch (error) {
                console.error('Error al obtener productos:', error);
            }
        },
        async submitForm() {
            try {
                if (this.editingProductId) {
                    // Editar producto
                    await axios.put(`${process.env.VUE_APP_API_URL}/api/edit-cleaning-product/${this.editingProductId}`, {
                        name: this.productName,
                        quantity: this.initialQuantity,
                        type: this.productType,
                        minimum: this.minimumStock
                    });
                } else {
                    // Agregar nuevo producto
                    await axios.post(`${process.env.VUE_APP_API_URL}/api/add-cleaning-product`, {
                        name: this.productName,
                        quantity: this.initialQuantity,
                        type: this.productType,
                        minimum: this.minimumStock
                    });
                }


                this.fetchProducts();
                this.resetForm();
            } catch (error) {
                console.error('Error al guardar el producto:', error);
            }
        },
        async deleteProduct(id) {
            if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
                try {
                    await axios.patch(`${process.env.VUE_APP_API_URL}/api/delete-cleaning-product/${id}`);
                    this.fetchProducts();  // Recargar la lista sin el producto desactivado
                } catch (error) {
                    console.error('Error al eliminar el producto:', error);
                }
            }
        },


        resetForm() {
            this.productName = '';
            this.initialQuantity = 0;
            this.editingProductId = null;
            this.productType = '';
            this.minimumStock = 0;

        }
    }
};
</script>

<style scoped>
.page-header {
    background: #0d6efd;
    color: white;
    border-radius: 1rem 1rem 0 0;
    /* redondear solo arriba */
}

.main-card {
    border-radius: 1rem;
}

.sub-card {
    border-radius: 0.8rem;
}

.scrollable-list {
    max-height: 420px;
    overflow-y: auto;
    border: 1px solid #e1e1e1;
    border-radius: 0.6rem;
}

.product-info {
    line-height: 1.1rem;
}

input[type="text"] {
    text-transform: uppercase;
}

.page-header {
    background: #0d6efd;
    color: white;
    border-radius: 1rem 1rem 0 0;
}

.home-btn {
    border-radius: 0.5rem;
    padding: 6px 14px;
    font-weight: bold;
}
</style>