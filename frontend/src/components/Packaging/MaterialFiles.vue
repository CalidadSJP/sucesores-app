<template>
    <div><br>
        <div class="text-center mb-4">
            <h1>Gestión de Archivos - Material de Empaque</h1>
        </div><br>
        <div class="container mt-4">
            <!-- Área para subir archivos dentro de una tarjeta -->
            <div class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h4 class="m-0">Subir archivo</h4>
                </div>
                <div class="card-body">
                    <form @submit.prevent="submitFile">
                        <div class="mb-3">
                            <label for="date" class="form-label">Fecha</label>
                            <input type="date" v-model="date" id="date" class="form-control" required />
                        </div>

                        <div class="mb-3">
                            <label for="brand" class="form-label">Marca</label>
                            <select v-model="brand" id="brand" class="form-select" required>
                                <option value="" disabled>Selecciona una marca</option>
                                <option v-for="brand in brands" :key="brand" :value="brand">
                                    {{ brand }}
                                </option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="supplier" class="form-label">Proveedor</label>
                            <select v-model="supplier" id="supplier" class="form-select" required>
                                <option value="" disabled>Selecciona un proveedor</option>
                                <option v-for="provider in providers" :key="provider" :value="provider">
                                    {{ provider }}
                                </option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="product" class="form-label">Producto</label>
                            <select v-model="product" id="product" class="form-select" required>
                                <option value="" disabled>Selecciona un producto</option>
                                <option v-for="product in products" :key="product" :value="product">
                                    {{ product }}
                                </option>
                            </select>
                        </div>


                        <div class="mb-3">
                            <label for="fileType" class="form-label">Tipo de archivo</label>
                            <select v-model="fileType" id="fileType" class="form-select" required>
                                <option value="" disabled>Selecciona el tipo de archivo</option>
                                <option value="factura_guia">Factura/Guía de remisión</option>
                                <option value="estado_camion">Imagen del Estado del Camión</option>
                                <option value="placa_camion">Imagen de la Placa del Camión</option>
                                <option value="ficha_certificado">Ficha Técnica/Certificado de Calidad</option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="file" class="form-label">Archivo</label>
                            <input type="file" @change="handleFileChange" id="file" class="form-control" required />
                        </div>
                        <br>
                        <div class="d-flex justify-content-center gap-3">
                            <button type="submit" class="btn btn-success">Aceptar</button>
                            <button type="button" @click="cancelUpload" class="btn btn-secondary">Limpiar</button>
                        </div>
                    </form>
                </div>
            </div>



            <!-- Listas de archivos dentro de tarjetas -->
            <div id="transporte" class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h5 class="m-0">Archivos - Transporte</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <label for="transporteFilter" class="form-label">Filtrar Archivos</label>
                        <input type="text" v-model="transporteFilter" id="transporteFilter" class="form-control"
                            placeholder="Buscar archivo..." />
                    </div>
                    <ul class="list-group">
                        <li v-for="file in paginatedTransporteFiles" :key="file"
                            class="list-group-item d-flex justify-content-between align-items-center">
                            <span @click="showImagePreview(file, 'Transporte')" class="text-primary"
                                style="cursor: pointer;">
                                {{ file }}
                            </span>

                            <div class="btn-group">
                                <!-- Botón de descarga -->
                                <a :href="generateDownloadUrl(file, 'Transporte')" class="btn btn-success btn-sm"
                                    :download="file">
                                    <img src="@/assets/download-icon.png" alt="Descargar" class="icon" />
                                </a>
                                <!-- Botón de eliminar -->
                                <button @click="confirmDelete(file, 'Transporte')" class="btn btn-danger btn-sm ms-2">
                                    <img src="@/assets/delete-icon.png" alt="Eliminar" class="icon" />
                                </button>
                            </div>
                        </li>
                    </ul>
                    <!-- Paginación de archivos en Transporte -->
                    <div class="pagination-container mt-4 d-flex justify-content-center align-items-center gap-2">
                        <button @click="previousPage('transporte')" class="pagination-btn"
                            :disabled="currentTransportePage <= 1">
                            Anterior
                        </button>

                        <ul class="pagination mb-0 d-flex gap-1">
                            <li v-for="page in visibleTransportePages" :key="page"
                                :class="['page-item-custom', { active: page === currentTransportePage }]">
                                <button @click="goToPage('transporte', page)" class="page-link-custom"
                                    :class="{ 'active-page': page === currentTransportePage }">
                                    {{ page }}
                                </button>
                            </li>
                        </ul>

                        <button @click="nextPage('transporte')" class="pagination-btn"
                            :disabled="currentTransportePage >= totalTransportePages">
                            Siguiente
                        </button>
                    </div>
                </div>
            </div>

            <div id="producto" class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h5 class="m-0">Archivos - Producto</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <label for="productoFilter" class="form-label">Filtrar Archivos</label>
                        <input type="text" v-model="productoFilter" id="productoFilter" class="form-control"
                            placeholder="Buscar archivo..." />
                    </div>
                    <ul class="list-group">
                        <li v-for="file in paginatedProductoFiles" :key="file"
                            class="list-group-item d-flex justify-content-between align-items-center">
                            <span @click="showImagePreview(file, 'Producto')" class="text-primary"
                                style="cursor: pointer;">
                                {{ file }}
                            </span>

                            <div class="btn-group">
                                <!-- Botón de descarga -->
                                <a :href="generateDownloadUrl(file, 'Producto')" class="btn btn-success btn-sm"
                                    :download="file">
                                    <img src="@/assets/download-icon.png" alt="Descargar" class="icon" />
                                </a>
                                <!-- Botón de eliminar -->
                                <button @click="confirmDelete(file, 'Producto')" class="btn btn-danger btn-sm ms-2">
                                    <img src="@/assets/delete-icon.png" alt="Eliminar" class="icon" />
                                </button>
                            </div>

                        </li>
                    </ul>
                    <!-- Paginación de archivos en Producto -->
                    <div class="pagination-container mt-4 d-flex justify-content-center align-items-center gap-2">
                        <button @click="previousPage('producto')" class="pagination-btn"
                            :disabled="currentProductoPage <= 1">
                            Anterior
                        </button>

                        <ul class="pagination mb-0 d-flex gap-1">
                            <li v-for="page in visibleProductoPages" :key="page"
                                :class="['page-item-custom', { active: page === currentProductoPage }]">
                                <button @click="goToPage('producto', page)" class="page-link-custom"
                                    :class="{ 'active-page': page === currentProductoPage }">
                                    {{ page }}
                                </button>
                            </li>
                        </ul>

                        <button @click="nextPage('producto')" class="pagination-btn"
                            :disabled="currentProductoPage >= totalProductoPages">
                            Siguiente
                        </button>
                    </div>

                </div>
            </div>
            <!-- Modal de vista previa de imagen o PDF -->
            <div class="modal fade" id="imagePreviewModal" tabindex="-1" aria-labelledby="imagePreviewLabel"
                aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="imagePreviewLabel">Vista Previa</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"
                                aria-label="Cerrar"></button>
                        </div>
                        <div class="modal-body text-center">

                            <!-- Si es PDF, usar iframe -->
                            <iframe v-if="isPdfPreview" :src="previewImageUrl" width="100%" height="480px"
                                style="border: none;">
                            </iframe>

                            <!-- Si es imagen, usar img con zoom -->
                            <img v-else-if="previewImageUrl" :src="previewImageUrl" alt="Vista previa"
                                :class="['img-fluid', zoomed ? 'zoomed-in' : '']" @click="toggleZoom"
                                style="max-width: 100%; max-height: 480px; cursor: zoom-in;" />

                            <!-- Si no es compatible -->
                            <p v-else>No es una imagen compatible para vista previa.</p>

                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import axios from "axios";
import * as bootstrap from 'bootstrap';

export default {
    data() {
        return {
            transporteFiles: [],
            productoFiles: [],
            selectedFolder: null,
            date: "",
            fileType: "",
            supplier: "",
            selectedFile: null,
            providers: [],
            transporteFilter: "", // Filtro para archivos en Transporte
            productoFilter: "",   // Filtro para archivos en Producto
            products: [], // Lista de productos
            product: "", // Producto seleccionado
            brand: "",
            brands: [],
            // Paginación
            currentTransportePage: 1,   // Página actual para Transporte
            currentProductoPage: 1,   // Página actual
            filesPerPage: 10,
            previewImageUrl: null,
            zoomed: false,
            isPdfPreview: false,
        };
    },
    computed: {
        paginatedTransporteFiles() {
            const filteredFiles = this.filteredTransporteFiles;
            const start = (this.currentTransportePage - 1) * this.filesPerPage;
            return filteredFiles.slice(start, start + this.filesPerPage);
        },
        paginatedProductoFiles() {
            const filteredFiles = this.filteredProductoFiles;
            const start = (this.currentProductoPage - 1) * this.filesPerPage;
            return filteredFiles.slice(start, start + this.filesPerPage);
        },
        filteredTransporteFiles() {
            return this.transporteFiles.filter(file =>
                file.toLowerCase().includes(this.transporteFilter.toLowerCase())
            );
        },
        // Filtrar los archivos de producto
        filteredProductoFiles() {
            return this.productoFiles.filter(file =>
                file.toLowerCase().includes(this.productoFilter.toLowerCase())
            );
        },
        visibleTransportePages() {
            const start = Math.floor((this.currentTransportePage - 1) / 3) * 3 + 1;
            const end = Math.min(start + 2, this.totalTransportePages);
            const pages = [];
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            return pages;
        },
        visibleProductoPages() {
            const start = Math.floor((this.currentProductoPage - 1) / 3) * 3 + 1;
            const end = Math.min(start + 2, this.totalProductoPages);
            const pages = [];
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            return pages;
        },
        totalTransportePages() {
            return Math.ceil(this.filteredTransporteFiles.length / this.filesPerPage);
        },
        totalProductoPages() {
            return Math.ceil(this.filteredProductoFiles.length / this.filesPerPage);
        },
    },
    mounted() {
        this.fetchFiles();
        this.fetchProviders();
        this.fetchProducts();
        this.fetchBrands();
    },
    methods: {
        toggleZoom() {
            this.zoomed = !this.zoomed;
        },
        async fetchFiles() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-material-files`);
                if (response.status === 200) {
                    // Ordenamos los archivos por fecha extraída del nombre
                    this.transporteFiles = this.sortFilesByDate(response.data.transporte_files);
                    this.productoFiles = this.sortFilesByDate(response.data.producto_files);

                    this.totalTransportePages = Math.ceil(this.transporteFiles.length / this.filesPerPage);
                    this.totalProductoPages = Math.ceil(this.productoFiles.length / this.filesPerPage);
                } else {
                    console.error("Error al obtener archivos.");
                }
            } catch (error) {
                console.error("Error al obtener archivos:", error);
                alert("Hubo un error al obtener los archivos. Inténtalo de nuevo.");
            }
        },
        // Función para ordenar archivos por fecha (extraída del nombre del archivo)
        sortFilesByDate(files) {
            return files.sort((a, b) => {
                const dateA = this.extractDateFromFileName(a);
                const dateB = this.extractDateFromFileName(b);
                return new Date(dateB) - new Date(dateA); // Orden descendente (más reciente primero)
            });
        },
        // Función para extraer la fecha del nombre del archivo (en formato 'dd-mm-yyyy')
        extractDateFromFileName(fileName) {
            const match = fileName.match(/^(\d{2}-\d{2}-\d{4})/); // Extrae la fecha en formato 'dd-mm-yyyy'
            if (match) {
                const dateParts = match[0].split('-'); // Separa el día, mes y año
                // Creamos una fecha con el formato 'yyyy-mm-dd' para que sea fácil de ordenar
                const formattedDate = `${dateParts[2]}-${dateParts[1]}-${dateParts[0]}`;
                return formattedDate;
            }
            return ''; // Si no encuentra la fecha, devuelve una cadena vacía
        },
        setFolder(folder) {
            this.selectedFolder = folder;
        },
        handleFileChange(event) {
            const selectedFile = event.target.files[0];
            if (selectedFile) {
                this.file = selectedFile; // Asigna el archivo seleccionado a la propiedad file
            } else {
                this.file = null; // En caso de que no se seleccione nada, resetea la propiedad
            }
        },
        formatDateToDDMMYYYY(date) {
            const [year, month, day] = date.split("-");
            return `${day}-${month}-${year}`;
        },
        async submitFile() {
            if (!this.file) {
                alert("Por favor, selecciona un archivo.");
                return;
            }

            try {
                const formData = new FormData();
                formData.append("supplier", this.supplier);
                formData.append("brand", this.brand);
                formData.append("fileType", this.fileType);
                formData.append("date", this.formatDateToDDMMYYYY(this.date)); // Convertir la fecha al formato correcto
                formData.append("product", this.product); // Añade el producto
                formData.append("file", this.file);

                // Llamada al backend para subir el archivo
                const response = await axios.post(
                    `${process.env.VUE_APP_API_URL}/api/submit-just-one-file-material`,
                    formData,
                    {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        },
                    }
                );

                if (response.status === 200) {
                    alert("Archivo subido exitosamente.");
                    this.cancelUpload(); // Resetea el formulario tras el éxito

                    // Llamar a fetchFiles para actualizar las listas después de la subida
                    this.fetchFiles(); // Actualiza las listas de archivos desde el backend

                } else {
                    alert("Error al subir el archivo. Inténtalo de nuevo.");
                }

            } catch (error) {
                console.error(error);
                if (error.response && error.response.data) {
                    alert(`Error: ${error.response.data.error}`);
                } else {
                    alert("Ocurrió un error al subir el archivo. Inténtalo de nuevo.");
                }
            }
        },
        resetForm() {
            this.selectedFile = null;
            this.date = null;
            this.fileType = null;
            this.supplier = '';
            this.selectedFolder = null;
            this.brand = '';
        },
        generateDownloadUrl(file, folder) {
            return `${process.env.VUE_APP_API_URL}/api/download-material-file/${folder}/${file}`;
        },
        goToPage(type, page) {
            if (type === 'transporte' && page >= 1 && page <= this.totalTransportePages) {
                this.currentTransportePage = page;
            } else if (type === 'producto' && page >= 1 && page <= this.totalProductoPages) {
                this.currentProductoPage = page;
            }
        },
        previousPage(type) {
            if (type === 'transporte' && this.currentTransportePage > 1) {
                this.currentTransportePage--;
            } else if (type === 'producto' && this.currentProductoPage > 1) {
                this.currentProductoPage--;
            }
        },
        nextPage(type) {
            if (type === 'transporte' && this.currentTransportePage < this.totalTransportePages) {
                this.currentTransportePage++;
            } else if (type === 'producto' && this.currentProductoPage < this.totalProductoPages) {
                this.currentProductoPage++;
            }
        },
        cancelUpload() {
            this.selectedFolder = null;
            this.date = "";
            this.fileType = "";
            this.supplier = "";
            this.selectedFile = null;
            this.product = "";
        },
        async confirmDelete(file, folder) {
            const confirmation = confirm(`¿Estás seguro de eliminar el archivo ${file}?`);
            if (confirmation) {
                this.deleteFile(file, folder);
            }
        },
        async deleteFile(file, folder) {
            try {
                const response = await axios.delete(`${process.env.VUE_APP_API_URL}/api/delete-material-file`, {
                    data: { file, folder }
                });
                if (response.status === 200) {
                    alert("Archivo eliminado.");
                    await this.fetchFiles();
                } else {
                    alert("Hubo un error al eliminar el archivo.");
                }
            } catch (error) {
                console.error("Error al eliminar el archivo:", error);
                alert("Hubo un error al eliminar el archivo. Inténtalo de nuevo.");
            }
        },
        async fetchProviders() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/provider-material`);
                if (response.status === 200) {
                    this.providers = response.data; // Asigna los proveedores obtenidos
                } else {
                    console.error("Error al obtener proveedores.");
                }
            } catch (error) {
                console.error("Error al obtener proveedores:", error);
            }
        },
        async fetchProducts() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-code`);
                if (response.status === 200) {
                    this.products = response.data; // Asigna los productos obtenidos
                } else {
                    console.error("Error al obtener productos.");
                }
            } catch (error) {
                console.error("Error al obtener productos:", error);
            }
        },
        async fetchBrands() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/brand`);
                this.brands = response.data; // Suponiendo que el backend devuelve un arreglo de strings
            } catch (error) {
                console.error('Error al obtener marcas:', error);
            }
        },
        async showImagePreview(file, folder) {
            const extension = file.split('.').pop().toLowerCase();
            const validExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'pdf'];

            if (!validExtensions.includes(extension)) {
                this.previewImageUrl = null;
                this.isPdfPreview = false;
                alert('Este archivo no es compatible para vista previa.');
                return;
            }

            const url = this.generateDownloadUrl(file, folder);
            this.isPdfPreview = extension === 'pdf';

            if (this.isPdfPreview) {
                // Descargar el PDF como Blob
                try {
                    const response = await fetch(url);
                    const blob = await response.blob();
                    this.previewImageUrl = URL.createObjectURL(blob); // ← crea URL temporal
                } catch (error) {
                    console.error('Error al cargar PDF:', error);
                    alert('No se pudo cargar el PDF para vista previa.');
                    return;
                }
            } else {
                this.previewImageUrl = url;
            }

            const modal = new bootstrap.Modal(document.getElementById('imagePreviewModal'));
            modal.show();
        }

    }
};
</script>

<style scoped>
.container {
    max-width: 900px;
    margin: 0 auto;
}

.card {
    max-width: 800px;
    margin-top: 20px;
}

.btn-active {
    background-color: #198754;
    /* Verde de éxito */
    border-color: #198754;
}

.icon {
    width: 20px;
    /* Ajusta el tamaño del icono */
    height: 20px;
    display: block;
    /* Hace que el icono ocupe el tamaño completo del contenedor */
    margin: 0 auto;
    /* Centra el icono en el botón */
}

.list-group-item {
    word-wrap: break-word;
    /* Permite dividir palabras largas */
    word-break: break-word;
    /* Alternativa para navegadores antiguos */
    overflow-wrap: break-word;
    /* Asegura compatibilidad con navegadores modernos */
}

/* Controla el diseño interno de cada ítem */
.list-group-item {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    /* Permite que el texto y los botones bajen de línea si es necesario */
}

/* Controla el texto de los nombres */
.list-group-item>span {
    flex: 1 1 auto;
    /* Ocupa el espacio disponible */
    min-width: 0;
    /* Permite que el texto largo se ajuste */
    text-overflow: ellipsis;
    /* Agrega puntos suspensivos si es muy largo */
    overflow: hidden;
    white-space: nowrap;
    /* Mantiene todo en una línea si hay espacio */
}

/* Botones para que se alineen correctamente y no se desborden */
.list-group-item .btn-group {
    flex-shrink: 0;
    /* Evita que los botones cambien de tamaño */
    display: flex;
}

.pagination-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.pagination-btn {
    background-color: #fff;
    color: #198754;
    border: 2px solid #198754;
    padding: 6px 14px;
    border-radius: 20px;
    transition: all 0.3s ease;
    font-weight: 600;
}

.pagination-btn:hover:not(:disabled) {
    background-color: #198754;
    color: #fff;
    box-shadow: 0 4px 12px rgba(25, 135, 84, 0.3);
}

.pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.page-item-custom {
    list-style: none;
}

.page-link-custom {
    border: none;
    background-color: #f8f9fa;
    color: #198754;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    font-weight: 500;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.page-link-custom:hover {
    background-color: #d1e7dd;
    color: #0f5132;
    cursor: pointer;
}

.active-page {
    background-color: #198754;
    color: #fff;
    font-weight: bold;
    box-shadow: 0 0 8px rgba(25, 135, 84, 0.5);
}

.zoomed-in {
    transform: scale(2);
    transition: transform 0.3s ease;
    cursor: zoom-out;
}
</style>