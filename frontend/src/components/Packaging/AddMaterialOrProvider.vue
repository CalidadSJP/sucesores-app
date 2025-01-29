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
                        <br><button class="btn btn-primary mt-2" @click="addProvider">Agregar Proveedor</button>
                    </div>

                    <!-- Sección para agregar producto -->
                    <div class="col-md-6 mb-3">
                        <h5>Agregar Producto</h5><br>

                        <label for="code" class="form-label">Codigo</label>
                        <input type="text" id="code" v-model="newCode" class="form-control"
                            @input="convertToUppercase('newCode')" placeholder="Ingrese el codigo del producto" />
                        <br>
                        <label for="code-sap" class="form-label">Codigo SAP</label>
                        <input type="text" id="code-sap" v-model="newCodeSap" class="form-control"
                            @input="convertToUppercase('newCodeSap')"
                            placeholder="Ingrese el codigo SAP del producto" />
                        <br>
                        <label for="product-name" class="form-label">Nombre del Producto</label>
                        <input type="text" id="product-name" v-model="newMaterialName" class="form-control"
                            @input="convertToUppercase('newMaterialName')"
                            placeholder="Ingrese el nombre del producto" />
                        <br>
                        <label for="product-type" class="form-label">Tipo de Producto</label>
                        <input type="text" id="product-type" v-model="newProductType" class="form-control"
                            @input="convertToUppercase('newProductType')" placeholder="Ingrese el tipo del producto" />

                        <div class="mt-3">
                            <label for="provider-id" class="form-label">Proveedor</label>
                            <select class="form-select" id="provider-id" v-model="newMaterialProvider" required>
                                <option value="" disabled>Seleccione...</option>
                                <option v-for="provider in providers" :key="provider.id" :value="provider.id">
                                    {{ provider.provider_name }}
                                </option>
                            </select>
                        </div>
                        <br>
                        <!-- Marca -->
                        <div class="mb-3">
                            <label for="brand-id" class="form-label">Marca</label>
                            <select class="form-select" id="brand-id" v-model="newBrand" required>
                                <option value="" disabled>Seleccione...</option>
                                <option v-for="brand in brands" :key="brand.id" :value="brand.id">
                                    {{ brand.brand_name }}
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
                <div class="mb-3">
                    <label for="filter" class="form-label">Filtrar productos</label>
                    <input type="text" id="filter" v-model="filterText" class="form-control"
                        placeholder="Buscar por nombre, proveedor o tipo de producto" />
                </div>

                <!-- Contenedor con desplazamiento horizontal -->
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th scope="col">Codigo</th>
                                <th scope="col">Code SAP</th>
                                <th scope="col">Nombre</th>
                                <th scope="col">Proveedor</th>
                                <th scope="col">Tipo de Producto</th>
                                <th scope="col">Marca</th>
                                <th scope="col">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="material in paginatedMaterials" :key="material.id">
                                <td>{{ material.code }}</td>
                                <td>{{ material.code_sap }}</td>
                                <td>{{ material.material_name }}</td>
                                <td>{{ material.provider_name }}</td>
                                <td>{{ material.material_type }}</td>
                                <td>{{ material.brand_name }}</td>
                                <td class="actions-column">
                                    <div class="action-buttons">
                                        <button class="btn btn-warning btn-sm"
                                            @click="editProduct(material)">Editar</button>
                                        <button class="btn btn-danger btn-sm ms-2"
                                            @click="confirmDeleteProduct(material.id)">Eliminar</button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Paginación -->
                <div class="pagination-container mt-3">
                    <nav aria-label="Page navigation">
                        <ul class="pagination justify-content-center">
                            <!-- Botón Anterior -->
                            <li class="page-item" :class="{ disabled: currentPage === 1 }">
                                <button class="page-link" @click="previousPage" aria-label="Anterior">
                                    Anterior
                                </button>
                            </li>

                            <!-- Página actual -->
                            <li class="page-item active">
                                <span class="page-link">{{ currentPage }}</span>
                            </li>

                            <!-- Botón Siguiente -->
                            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                                <button class="page-link" @click="nextPage" aria-label="Siguiente">
                                    Siguiente
                                </button>
                            </li>
                        </ul>
                    </nav>
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


                    <label for="new-code" class="form-label">Codigo</label>
                    <input type="text" id="new-code" v-model="materialToEdit.code" class="form-control"
                        style="text-transform: uppercase;" required placeholder="Ingrese el codigo del producto" />
                    <br>
                    <label for="new-code-sap" class="form-label">Codigo SAP</label>
                    <input type="text" id="new-code-sap" v-model="materialToEdit.code_sap" class="form-control"
                        style="text-transform: uppercase;" required placeholder="Ingrese el codigo SAP del producto" />

                    <div class="mb-3">
                        <label for="new-productName" class="form-label">Nombre del Producto</label>
                        <input type="text" id="new-productName" class="form-control"
                            v-model="materialToEdit.material_name" style="text-transform: uppercase;" required />
                    </div>

                    <label for="new-product-type" class="form-label">Tipo de Producto</label>
                    <input type="text" id="new-product-type" v-model="materialToEdit.material_type" class="form-control"
                        style="text-transform: uppercase;" required placeholder="Ingrese el tipo del producto" />


                    <div class="mb-3">
                        <label for="new-provider" class="form-label">Proveedor</label>
                        <select id="new-provider" class="form-select" v-model="materialToEdit.provider_id" required>
                            <option v-for="provider in providers" :key="provider.id" :value="provider.id">
                                {{ provider.provider_name }}
                            </option>
                        </select>
                    </div>
                    <!-- Marca -->
                    <div class="mb-3">
                        <label for="new-brand-id" class="form-label">Marca</label>
                        <select class="form-select" id="new-brand-id" v-model="materialToEdit.brand_id" required>
                            <option value="" disabled>Seleccione...</option>
                            <option v-for="brand in brands" :key="brand.id" :value="brand.id">
                                {{ brand.brand_name }}
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
            newCode: "",
            newCodeSap: "",
            newProvider: "",
            newMaterialName: "",
            newProductType: "",
            newBrand: "",
            newMaterialProvider: "",
            providers: [],
            materials: [],
            brands: [],
            materialToEdit: null, // Producto seleccionado para editar
            currentPage: 1,        // Página actual
            itemsPerPage: 15,      // Productos por página
            filterText: "",        // Texto para filtrar productos
        };
    },
    computed: {
        // Calcular el total de páginas
        totalPages() {
            return Math.ceil(this.filteredMaterials.length / this.itemsPerPage);
        },
        // Filtrar los materiales según el texto de búsqueda
        filteredMaterials() {
            const searchText = this.filterText.toLowerCase();
            return this.materials.filter(material => {
                return (
                    material.code.toLowerCase().includes(searchText) ||
                    material.code_sap.toLowerCase().includes(searchText) ||
                    material.material_name.toLowerCase().includes(searchText) ||
                    material.provider_name.toLowerCase().includes(searchText) ||
                    material.material_type.toLowerCase().includes(searchText) ||
                    material.brand_name.toLowerCase().includes(searchText)
                );
            });
        },
        // Calcular los materiales que se deben mostrar en la página actual
        paginatedMaterials() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.filteredMaterials.slice(start, end);
        }
    },
    created() {
        this.fetchProviders();
        this.fetchProducts();
        this.fetchBrands();
    },
    methods: {
        async fetchBrands() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-brand-material`);
                this.brands = response.data; // Suponiendo que el backend devuelve un arreglo de strings
            } catch (error) {
                console.error('Error al obtener marcas:', error);
            }
        },
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
                        code: this.newCode,
                        code_sap: this.newCodeSap,
                        material_name: this.newMaterialName,
                        provider_id: this.newMaterialProvider,
                        material_type: this.newProductType,
                        brand_id: this.newBrand
                    });
                    this.materials.push(response.data);
                    // Ordenar la lista después de agregar
                    this.materials.sort((a, b) => a.id - b.id);
                    this.newMaterialName = ""; // Limpiar campo
                    this.newMaterialProvider = ""; // Limpiar campo
                    this.newProductType = "";
                    this.newBrand = "";
                    this.newCode = "";
                    this.newCodeSap = "";
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
        },
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
        },
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
                        code: this.materialToEdit.code,
                        code_sap: this.materialToEdit.code_sap,
                        material_name: this.materialToEdit.material_name.toUpperCase(),
                        provider_id: this.materialToEdit.provider_id,
                        material_type: this.materialToEdit.material_type.toUpperCase(),
                        brand_id: this.materialToEdit.brand_id
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
        previousPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        }
    },
    mounted() {
        this.fetchProviders(); // Obtener la lista de proveedores al cargar
        this.fetchBrands(); // Obtener la lista de proveedores al cargar
    }
};
</script>

<style scoped>
.card {
    margin-bottom: 20px;
    border-radius: 10px;
    max-width: 1140px;
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

.pagination-container {
    margin-top: 20px;
}

.pagination .page-item {
    margin: 0 5px;
    /* Espaciado entre los botones */
}

.pagination .page-item .page-link {
    border-radius: 20px;
    /* Bordes redondeados */
    font-size: 16px;
    /* Tamaño de fuente adecuado */
    padding: 8px 18px;
    /* Ajusta el tamaño del botón */
    text-align: center;
    /* Asegura que el texto esté centrado */
    background-color: #f8f9fa;
    /* Color de fondo normal */
    color: #007bff;
    /* Color de texto por defecto */
    border: 2px solid #007bff;
    /* Borde azul */
    transition: background-color 0.3s, color 0.3s, border 0.3s;
    /* Efectos de transición */
}

.pagination .page-item .page-link:hover {
    background-color: #007bff;
    /* Fondo azul cuando se pasa el ratón */
    color: #fff;
    /* Cambia el texto a blanco cuando se pasa el ratón */
    border-color: #0056b3;
    /* Cambia el borde a un azul más oscuro */
}

.pagination .page-item.active .page-link {
    background-color: #007bff;
    /* Color de fondo cuando la página está activa */
    color: #fff;
    /* Color del texto cuando la página está activa */
    border-color: #007bff;
    /* Borde azul para la página activa */
}

.pagination .page-item.disabled .page-link {
    background-color: #e0e0e0;
    /* Color de fondo cuando el botón está deshabilitado */
    color: #6c757d;
    /* Color del texto cuando el botón está deshabilitado */
    border-color: #ddd;
    /* Color del borde cuando el botón está deshabilitado */
}

.pagination .page-item .page-link:focus {
    outline: none;
    /* Eliminar el borde al enfocar el botón */
    box-shadow: 0 0 0 0.2rem rgba(38, 143, 255, 0.5);
    /* Sombra suave azul */
}

.actions-column {
    vertical-align: middle;
    /* Asegura la alineación vertical de las filas */
    text-align: center;
    /* Centra el contenido horizontalmente */
}

/* Flexbox para alinear botones */
.action-buttons {
    display: flex;
    justify-content: center;
    /* Botones centrados horizontalmente */
    align-items: center;
    /* Botones centrados verticalmente */
    gap: 1px;
    /* Espaciado entre los botones */
}

/* Opcional: Asegurar altura uniforme para todas las filas */
.table tbody tr {
    height: 50px;
    /* Ajusta según el diseño general */
}
</style>