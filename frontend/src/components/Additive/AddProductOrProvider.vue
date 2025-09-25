<template>
    <div class="container mt-5">
        <h2 class="text-center mb-5">Gestión de Proveedores y Productos</h2>

        <!-- Tarjeta para agregar proveedores y productos -->
        <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5>Agregar</h5>
                <div>
                    <button @click="logout" class="btn btn-danger">
                        <i class="fas fa-sign-out-alt"></i> Cerrar sesión
                    </button>
                </div>
            </div>
            <div class="card-body">
                <div class="row">
                    <!-- Sección para agregar proveedor -->
                    <div class="col-md-6 mb-3">
                        <h5>Agregar Proveedor</h5><br>
                        <label for="provider-name" class="form-label">Nombre del Proveedor</label>
                        <input type="text" id="provider-name" v-model="newProvider" class="form-control"
                            @input="convertToUppercase('newProvider')" placeholder="Ingrese el nombre del proveedor" />
                        <button class="btn btn-primary mt-2" @click="addProvider">Agregar Proveedor</button>
                    </div>

                    <!-- Sección para agregar producto -->
                    <div class="col-md-6 mb-3">
                        <h5>Agregar Producto</h5><br>
                        <label for="product-name" class="form-label">Nombre del Producto</label>
                        <input type="text" id="product-name" v-model="newProductName" class="form-control"
                            @input="convertToUppercase('newProductName')"
                            placeholder="Ingrese el nombre del producto" />

                        <div class="mt-3">
                            <label for="provider-id" class="form-label">Proveedor</label>
                            <select class="form-select" id="provider-id" v-model="newProductProvider" required>
                                <option value="" disabled>Seleccione...</option>
                                <option v-for="provider in providers" :key="provider.id" :value="provider.id">
                                    {{ provider.provider_name }}
                                </option>
                            </select>
                        </div>

                        <div class="mt-3">
                            <label for="product-type" class="form-label">Tipo de Producto</label>
                            <select class="form-select" id="product-type" v-model="newProductType" required>
                                <option value="" disabled>Seleccione el tipo de producto...</option>
                                <option value="ADITIVO">ADITIVO</option>
                                <option value="MATERIAL DE EMPAQUE">MATERIA PRIMA</option>
                            </select>
                        </div>

                        <button class="btn btn-primary mt-3" @click="addProduct">Agregar Producto</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tarjeta para listar proveedores -->
        <div class="card mb-4">
            <div class="card-header">
                <h5>Lista de Proveedores</h5>
            </div>
            <div class="card-body">
                <ul class="list-group">
                    <li v-for="provider in providers" :key="provider.id"
                        class="list-group-item d-flex justify-content-between align-items-center">
                        {{ provider.provider_name }}
                        <div class="d-flex">
                            <button class="btn btn-warning btn-sm" @click="editProvider(provider)">Editar</button>
                            <button class="btn btn-danger btn-sm"
                                @click="confirmDeleteProvider(provider.id)">Eliminar</button>
                        </div>
                    </li>
                </ul>
            </div>
        </div>

        <!-- Tarjeta para listar productos -->
        <div class="card mb-4">
            <div class="card-header">
                <h5>Lista de Productos</h5>
            </div>
            <div class="card-body">
                <!-- Contenedor con desplazamiento horizontal -->
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th scope="col">Nombre del Producto</th>
                                <th scope="col">Proveedor</th>
                                <th scope="col">Tipo de Producto</th>
                                <th scope="col">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="product in products" :key="product.id">
                                <td>{{ product.product_name }}</td>
                                <td>{{ product.provider_name }}</td>
                                <td>{{ product.product_type }}</td>
                                <td class="d-flex">
                                    <!-- Botón para abrir la tarjeta de edición -->
                                    <button class="btn btn-warning btn-sm" @click="editProduct(product)">Editar</button>
                                    <button class="btn btn-danger btn-sm ms-2"
                                        @click="confirmDeleteProduct(product.id)">Eliminar</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Tarjeta para editar producto -->
        <div v-if="productToEdit" class="card mt-4" ref="editProductCard">
            <div class="card-header">
                <h5>Editar Producto</h5>
            </div>
            <div class="card-body">
                <form @submit.prevent="saveProductEdits">
                    <div class="mb-3">
                        <label for="productName" class="form-label">Nombre del Producto</label>
                        <input type="text" id="productName" class="form-control" v-model="productToEdit.product_name"
                            style="text-transform: uppercase;" required />
                    </div>
                    <div class="mb-3">
                        <label for="provider" class="form-label">Proveedor</label>
                        <select id="provider" class="form-select" v-model="productToEdit.provider_id" required>
                            <option v-for="provider in providers" :key="provider.id" :value="provider.id">
                                {{ provider.provider_name }}
                            </option>
                        </select>
                    </div><br>
                    <div class="d-flex justify-content-between">
                        <button type="submit" class="btn btn-success w-50 me-2">Guardar Cambios</button>
                        <button type="button" class="btn btn-secondary w-50" @click="cancelEdit">
                            Cancelar
                        </button>
                    </div>
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
            newProvider: "",
            newProductName: "",
            newProductProvider: "",
            newProductType: "",
            providers: [],
            products: [],
            productToEdit: null, // Producto seleccionado para editar
        };
    },
    created() {
        this.fetchProviders();
        this.fetchProducts();
    },
    methods: {
        async fetchProviders() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-providers`);
                // Ordenar los proveedores por ID
                this.providers = response.data.sort((a, b) => a.id - b.id);
            } catch (error) {
                console.error("Error al obtener proveedores:", error);
            }
        },
        async fetchProducts() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-products`);
                // Ordenar los productos por ID
                this.products = response.data.sort((a, b) => a.id - b.id);
            } catch (error) {
                console.error("Error al obtener productos:", error);
            }
        },
        convertToUppercase(field) {
            this[field] = this[field].toUpperCase();
        },
        async addProvider() {
            if (this.newProvider) {
                try {
                    const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/add-provider`, {
                        provider_name: this.newProvider,
                    });
                    this.providers.push(response.data);
                    // Ordenar la lista después de agregar
                    this.providers.sort((a, b) => a.id - b.id);
                    this.newProvider = ""; // Limpiar campo
                } catch (error) {
                    console.error("Error al agregar proveedor:", error);
                }
            }
        },
        async addProduct() {
            if (this.newProductName && this.newProductProvider && this.newProductType) {
                try {
                    const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/add-product`, {
                        product_name: this.newProductName,
                        provider_id: this.newProductProvider,
                        product_type: this.newProductType,
                    });
                    this.products.push(response.data);
                    // Ordenar la lista después de agregar
                    this.products.sort((a, b) => a.id - b.id);
                    this.newProductName = ""; // Limpiar campo
                    this.newProductProvider = ""; // Limpiar campo
                    this.newProductType = "";
                } catch (error) {
                    console.error("Error al agregar producto:", error);
                }
            }
        },
        async confirmDeleteProvider(id) {
            if (confirm("¿Estás seguro de que deseas eliminar este proveedor?")) {
                try {
                    await axios.delete(`${process.env.VUE_APP_API_URL}/api/delete-provider/${id}`);
                    this.providers = this.providers.filter(provider => provider.id !== id);
                    // Ordenar la lista después de eliminar
                    this.providers.sort((a, b) => a.id - b.id);
                } catch (error) {
                    console.error("Error al eliminar proveedor:", error);
                }
            }
        },
        async confirmDeleteProduct(id) {
            if (confirm("¿Estás seguro de que deseas eliminar este producto?")) {
                try {
                    await axios.delete(`${process.env.VUE_APP_API_URL}/api/delete-product/${id}`);
                    this.products = this.products.filter(product => product.id !== id);
                    // Ordenar la lista después de eliminar
                    this.products.sort((a, b) => a.id - b.id);
                } catch (error) {
                    console.error("Error al eliminar producto:", error);
                }
            }
        },
        editProvider(provider) {
            const newName = prompt("Editar nombre del proveedor", provider.provider_name);
            if (newName && newName !== provider.provider_name) {
                this.updateProvider(provider.id, newName);
            }
        },
        async updateProvider(id, newName) {
            try {
                const response = await axios.put(`${process.env.VUE_APP_API_URL}/api/update-provider/${id}`, {
                    provider_name: newName,
                });
                // Encuentra y actualiza el proveedor
                const index = this.providers.findIndex(provider => provider.id === id);
                if (index !== -1) {
                    this.providers[index].provider_name = response.data.provider_name;
                }
                // Ordenar la lista después de la actualización
                this.providers.sort((a, b) => a.id - b.id);
            } catch (error) {
                console.error("Error al editar proveedor:", error);
            }
        },
        editProduct(product) {
            this.productToEdit = { ...product }; // Crear copia del producto

            this.$nextTick(() => {
                const editCard = this.$refs.editProductCard;
                if (editCard) {
                    editCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        },
        async saveProductEdits() {
            try {
                // Enviar cambios al backend
                const response = await axios.put(
                    `${process.env.VUE_APP_API_URL}/api/update-product/${this.productToEdit.id}`,
                    {
                        product_name: this.productToEdit.product_name.toUpperCase(),
                        provider_id: this.productToEdit.provider_id,
                    }
                );

                // Actualizar la lista de productos con la respuesta
                const index = this.products.findIndex(
                    (product) => product.id === this.productToEdit.id
                );
                if (index !== -1) {
                    this.products[index] = response.data;
                }

                // Limpiar selección
                this.productToEdit = null;
            } catch (error) {
                console.error("Error al guardar cambios del producto:", error);
            }
        },
        cancelEdit() {
            this.productToEdit = null; // Cancelar edición
        },
        logout() {
            // Limpia el almacenamiento local y redirige al usuario
            localStorage.removeItem('authToken'); // Elimina el token
            localStorage.removeItem('user_area'); // Elimina el área
            localStorage.removeItem('user_id'); // Elimina el ID del usuario
            this.$router.push('/additive-home'); // Redirige al login
        }
    },
    mounted() {
        this.fetchProviders(); // Obtener la lista de proveedores al cargar
    }
};
</script>

<style scoped>
.card {
    margin-bottom: 20px;
    border-radius: 10px;
    max-width: 900px;
}

.card-header {
    font-size: 1.25rem;
    font-weight: bold;
}

.card-body {
    padding: 1.25rem;
}

.list-group-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.list-group-item button {
    margin-left: 10px;
}

.btn {
    width: 100%;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}
</style>