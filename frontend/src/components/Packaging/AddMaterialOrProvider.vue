<template>
    <div class="container mt-5">
        <h2 class="text-center mb-5">Gestión de Proveedores y Material de Empaque</h2>

        <!-- Tarjeta para agregar proveedores y productos -->
        <div class="card mb-4">
            <div class="card-header">
                <h5>Agregar</h5>
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
                        <input type="text" id="product-name" v-model="newMaterialName" class="form-control"
                            @input="convertToUppercase('newMaterialName')"
                            placeholder="Ingrese el nombre del producto" />

                        <div class="mt-3">
                            <label for="provider-id" class="form-label">Proveedor</label>
                            <select class="form-select" id="provider-id" v-model="newMaterialProvider" required>
                                <option value="" disabled>Seleccione...</option>
                                <option v-for="provider in providers" :key="provider.id" :value="provider.id">
                                    {{ provider.provider_name }}
                                </option>
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
                            <tr v-for="material in materials" :key="material.id">
                                <td>{{ material.material_name }}</td>
                                <td>{{ material.provider_name }}</td>
                                <td>{{ material.material_type }}</td>
                                <td class="d-flex">
                                    <!-- Botón para abrir la tarjeta de edición -->
                                    <button class="btn btn-warning btn-sm" @click="editProduct(material)">Editar</button>
                                    <button class="btn btn-danger btn-sm ms-2"
                                        @click="confirmDeleteProduct(material.id)">Eliminar</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Tarjeta para editar producto -->
        <div v-if="materialToEdit" class="card mt-4" ref="editProductCard">
            <div class="card-header">
                <h5>Editar Producto</h5>
            </div>
            <div class="card-body">
                <form @submit.prevent="saveProductEdits">
                    <div class="mb-3">
                        <label for="productName" class="form-label">Nombre del Producto</label>
                        <input type="text" id="productName" class="form-control" v-model="materialToEdit.material_name"
                            style="text-transform: uppercase;" required />
                    </div>
                    <div class="mb-3">
                        <label for="provider" class="form-label">Proveedor</label>
                        <select id="provider" class="form-select" v-model="materialToEdit.provider_id" required>
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
            newMaterialName: "",
            newMaterialProvider: "",
            providers: [],
            materials: [],
            materialToEdit: null, // Producto seleccionado para editar
        };
    },
    created() {
        this.fetchProviders();
        this.fetchProducts();
    },
    methods: {
        async fetchProviders() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-providers-material`);
                // Ordenar los proveedores por ID
                this.providers = response.data.sort((a, b) => a.id - b.id);
            } catch (error) {
                console.error("Error al obtener proveedores:", error);
            }
        },

        async fetchProducts() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-materials`);
                // Ordenar los productos por ID
                this.materials = response.data.sort((a, b) => a.id - b.id);
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
                    const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/add-provider-material`, {
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
            if (this.newMaterialName && this.newMaterialProvider) {
                try {
                    const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/add-material`, {
                        material_name: this.newMaterialName,
                        provider_id: this.newMaterialProvider,
                    });
                    this.materials.push(response.data);
                    // Ordenar la lista después de agregar
                    this.materials.sort((a, b) => a.id - b.id);
                    this.newMaterialName = ""; // Limpiar campo
                    this.newMaterialProvider = ""; // Limpiar campo
                } catch (error) {
                    console.error("Error al agregar producto:", error);
                }
            }
        },

        async confirmDeleteProvider(id) {
            if (confirm("¿Estás seguro de que deseas eliminar este proveedor?")) {
                try {
                    await axios.delete(`${process.env.VUE_APP_API_URL}/api/delete-provider-material/${id}`);
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
                    await axios.delete(`${process.env.VUE_APP_API_URL}/api/delete-material/${id}`);
                    this.materials = this.materials.filter(material => material.id !== id);
                    // Ordenar la lista después de eliminar
                    this.materials.sort((a, b) => a.id - b.id);
                } catch (error) {
                    console.error("Error al eliminar producto:", error);
                }
            }
        }
        ,
        editProvider(provider) {
            const newName = prompt("Editar nombre del proveedor", provider.provider_name);
            if (newName && newName !== provider.provider_name) {
                this.updateProvider(provider.id, newName);
            }
        },

        async updateProvider(id, newName) {
            try {
                const response = await axios.put(`${process.env.VUE_APP_API_URL}/api/update-provider-material/${id}`, {
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
        }

        ,
        editProduct(material) {
            this.materialToEdit = { ...material }; // Crear copia del producto

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
                    `${process.env.VUE_APP_API_URL}/api/update-material/${this.materialToEdit.id}`,
                    {
                        material_name: this.materialToEdit.material_name.toUpperCase(),
                        provider_id: this.materialToEdit.provider_id,
                    }
                );

                // Actualizar la lista de productos con la respuesta
                const index = this.materials.findIndex(
                    (material) => material.id === this.materialToEdit.id
                );
                if (index !== -1) {
                    this.materials[index] = response.data;
                }

                // Limpiar selección
                this.materialToEdit = null;
            } catch (error) {
                console.error("Error al guardar cambios del producto:", error);
            }
        },
        cancelEdit() {
            this.materialToEdit = null; // Cancelar edición
        },
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