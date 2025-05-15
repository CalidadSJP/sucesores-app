<template>
    <div class="container mt-5">
        <h2 class="my-4 text-center">Listado de Productos</h2>

        <!-- Tarjeta contenedora -->
        <div class="card p-4 shadow-lg">
            <div class="row">
                <!-- Tarjeta: Lista de productos -->
                <div class="col-md-7 mb-4">
                    <div class="card p-3 shadow-sm h-100">
                        <div class="scrollable-list">
                            <ul class="list-group">
                                <li v-for="product in products" :key="product.id"
                                    class="list-group-item d-flex justify-content-between align-items-center">
                                    <div>
                                        <strong>{{ product.name }}</strong>
                                        <br>
                                        <small class="text-muted">Cantidad: {{ product.quantity }}</small>
                                        <br>
                                        <small class="text-muted">Tipo: {{ product.type }}</small>
                                    </div>
                                    <div class="btn-group" role="group">
                                        <button class="btn btn-sm btn-outline-primary" @click="selectProduct(product)">
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

                <!-- Tarjeta: Formulario para añadir o editar -->
                <div class="col-md-5">
                    <div class="card p-3 shadow-sm d-flex flex-column justify-content-between">
                        <div>
                            <h5 class="card-title mb-3">{{ editingProductId ? 'Editar Producto' : 'Nuevo Producto' }}
                            </h5>
                            <form @submit.prevent="submitForm">
                                <div class="mb-3">
                                    <label for="productName" class="form-label">Nombre del Producto</label>
                                    <input type="text" class="form-control text-uppercase" id="productName"
                                        v-model="productName" required>
                                </div>

                                <div class="mb-3">
                                    <label for="initialQuantity" class="form-label">Cantidad Inicial</label>
                                    <input type="number" class="form-control" id="initialQuantity"
                                        v-model="initialQuantity" required min="0">
                                </div>

                                <div class="mb-3">
                                    <label for="productType" class="form-label">Tipo</label>
                                    <select class="form-select" id="productType" v-model="productType" required>
                                        <option disabled value="">Selecciona un tipo</option>
                                        <option value="PAPEL">PAPEL</option>
                                        <option value="INSECTICIDAS">INSECTICIDAS</option>
                                        <option value="JABONES Y DESINFECTANTES">JABONES Y DESINFECTANTES</option>
                                        <option value="ESCOBAS Y TRAPEADORES">ESCOBAS Y TRAPEADORES</option>
                                    </select>
                                </div>


                                <button type="submit" class="btn btn-success w-100">
                                    <i class="fas fa-save"></i> {{ editingProductId ? 'Actualizar' : 'Agregar' }}
                                </button>
                                <!-- Botón para limpiar el formulario -->
                                <button v-if="editingProductId" class="btn btn-secondary mt-2 w-100" @click="resetForm">
                                    Cancelar Edición
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div><br><br>
    </div>
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
            editingProductId: null,
        };
    },
    created() {
        this.fetchProducts();
    },
    methods: {
        selectProduct(product) {
            this.editingProductId = product.id;
            this.productName = product.name;
            this.initialQuantity = product.quantity;
            this.productType = product.type;
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
                    });
                } else {
                    // Agregar nuevo producto
                    await axios.post(`${process.env.VUE_APP_API_URL}/api/add-cleaning-product`, {
                        name: this.productName,
                        quantity: this.initialQuantity,
                        type: this.productType
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
                    await axios.delete(`${process.env.VUE_APP_API_URL}/api/delete-cleaning-product/${id}`);
                    this.fetchProducts();
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
        }
    }
};
</script>

<style scoped>
input[type="text"] {
    text-transform: uppercase;
}

.card {
    border-radius: 1rem;
}

.card-title {
    font-weight: bold;
}

.list-group-item {
    font-size: 1rem;
}

.scrollable-list {
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid #dee2e6;
    border-radius: 0.5rem;
}
</style>