<template>
    <div class="container">
        <h2 class="text-center mb-4">Control de Humedades - Pastificio</h2>

        <!-- Tarjeta para ingreso -->
        <div class="card mb-4">
            <div class="card-header bg-success text-white">
                <h3>Formulario de Registro</h3>
            </div>
            <div class="card-body">
                <form @submit.prevent="confirmAndSubmit">
                    <div class="row">
                        <div class="form-group col-md-2">
                            <label for="date" class="form-label">Fecha</label>
                            <input v-model="form.date" type="date" class="form-control" required />
                        </div>
                        <div class="form-group col-md-2">
                            <label for="time" class="form-label">Hora</label>
                            <input v-model="form.time" type="time" class="form-control" required />
                        </div>
                        <br><br><br>
                        <div class="form-group col-md-2">
                            <label for="line" class="form-label">Linea</label>
                            <select id="line" class="form-control" v-model="form.line">
                                <option v-for="line in lines" :key="line.id" :value="line.line_name">
                                    {{ line.line_name }}
                                </option>
                            </select>
                        </div>
                        <div class="form-group col-md-4">
                            <label for="format" class="form-label">Formato</label>
                            <select v-model="form.format" class="form-control">
                                <option v-for="format in formats" :key="format.id" :value="format.format_name">
                                    {{ format.format_name }}
                                </option>
                            </select>
                        </div>
                        <div class="form-group col-md-2">
                            <label for="zone" class="form-label">Zona</label>
                            <select v-model="form.zone" class="form-control" required>
                                <option>SALIDA</option>
                                <option>PRESECADO</option>
                                <option>CINTA/PISO 1</option>
                            </select>
                        </div>
                    </div><br>
                    <div class="row">
                        <!-- Termobalanza -->
                        <div class="form-group col-md-2">
                            <label for="balance" class="form-label">Termobalanza</label>
                            <select v-model="form.balance" class="form-control" required>
                                <option>TB-03</option>
                                <option>TB-04</option>
                            </select>
                        </div>
                        <div class="form-group col-md-2">
                            <label for="humidity" class="form-label">Humedad (%)</label>
                            <input v-model="form.humidity" type="number" step="0.01" class="form-control" required />
                        </div>
                        <div class="form-group col-md-8">
                            <label for="responsible" class="form-label">Responsable</label>
                            <input v-model="form.responsible" type="text" class="form-control" required />
                        </div><br><br><br><br>
                        <div class="form-group col-md-12">
                            <label for="observations" class="form-label">Observaciones</label>
                            <textarea v-model="form.observations" class="form-control" rows="4"></textarea>
                        </div>
                    </div>
                    <div class="mt-3 d-flex gap-2">
                        <button type="submit" class="btn btn-success">Guardar</button>
                        <button type="button" @click="resetForm" class="btn btn-secondary">Limpiar</button>
                    </div>

                </form>
            </div>
        </div>

        <!-- Tarjeta para mostrar registros -->
        <div class="card">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0">Registro</h5>
                    <button @click="showLoginModal = true" class="btn btn-primary">
                        Descargar
                    </button>
                </div><br>
                <!-- Contenedor desplazable -->
                <div class="table-responsive">
                    <table class="table table-bordered table-striped">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Termobalanza</th>
                                <th>Fecha</th>
                                <th>Hora</th>
                                <th>Línea</th>
                                <th>Formato</th>
                                <th>Zona</th>
                                <th>% Humedad</th>
                                <th>Responsable</th>
                                <th>Observaciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="record in records" :key="record.id">
                                <td>{{ record.id }}</td>
                                <td>{{ record.balance }}</td>
                                <td>{{ record.date }}</td>
                                <td>{{ record.time }}</td>
                                <td>{{ record.line }}</td>
                                <td>{{ record.format }}</td>
                                <td>{{ record.zone }}</td>
                                <td>{{ record.humidity }}</td>
                                <td>{{ record.responsible }}</td>
                                <td>{{ record.observations }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <!-- Barra de Paginación -->
                <div class="pagination-container mt-4 d-flex justify-content-center align-items-center gap-2">
                    <button @click="previousPage" class="pagination-btn" :disabled="currentPage <= 1">
                        Anterior
                    </button>

                    <ul class="pagination mb-0 d-flex gap-1">
                        <li v-for="page in visiblePages" :key="page"
                            :class="['page-item-custom', { active: page === currentPage }]">
                            <button @click="goToPage(page)" class="page-link-custom"
                                :class="{ 'active-page': page === currentPage }">
                                {{ page }}
                            </button>
                        </li>
                    </ul>

                    <button @click="nextPage" class="pagination-btn" :disabled="currentPage >= totalPages">
                        Siguiente
                    </button>
                </div>
            </div>
        </div>
        <div v-if="showLoginModal" class="login-modal">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Descarga del Registro de Humedades</h5>
                    </div><br>
                    <div class="modal-body">
                        <form @submit.prevent="authenticate">
                            <div class="mb-3">
                                <label for="username" class="form-label">Usuario</label>
                                <input type="text" id="username" v-model="username" class="form-control" required />
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Contraseña</label>
                                <input type="password" id="password" v-model="password" class="form-control" required />
                            </div>
                            <div class="d-flex justify-content-between">
                                <button type="submit" class="btn btn-success w-45">Iniciar Sesión</button>
                                <button type="button" class="btn btn-secondary w-45"
                                    @click="showLoginModal = false">Cancelar</button>
                            </div>
                        </form>
                        <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            form: {
                balance: '',
                date: '',
                time: '',
                format: '',
                zone: '',
                humidity: '',
                responsible: '',
                observations: '',
                line: '',

            },
            lines: [],
            recordsAll: [],
            formats: [],
            currentPage: 1,
            recordsPerPage: 30,
            showLoginModal: false,
            username: "",
            password: "",
            errorMessage: "",

        }
    },
    watch: {
        'form.line': function (newLineName) {
            const selectedLine = this.lines.find(line => line.line_name === newLineName)
            if (selectedLine) {
                this.fetchFormats(selectedLine.id)
            } else {
                this.formats = []
            }
        }
    },
    computed: {
        totalPages() {
            return Math.ceil(this.recordsAll.length / this.recordsPerPage)
        },
        visiblePages() {
            const total = this.totalPages
            const current = this.currentPage
            const groupSize = 3

            const startGroup = Math.floor((current - 1) / groupSize) * groupSize + 1
            const endGroup = Math.min(startGroup + groupSize - 1, total)

            const pages = []
            for (let i = startGroup; i <= endGroup; i++) {
                pages.push(i)
            }
            return pages
        },
        records() {
            const start = (this.currentPage - 1) * this.recordsPerPage
            const end = start + this.recordsPerPage
            return this.recordsAll.slice(start, end)
        }
    },
    methods: {
        async confirmAndSubmit() {
            if (confirm('¿Estás seguro de guardar este registro?')) {
                try {
                    // Convertir los campos deseados a mayúsculas
                    this.form.responsible = this.form.responsible.toUpperCase()
                    this.form.observations = this.form.observations.toUpperCase()

                    await axios.post(`${process.env.VUE_APP_API_URL}/api/submit-humidity-control`, this.form)
                    alert('Registro guardado exitosamente.')
                    this.loadRecords()
                    this.resetForm()
                } catch (error) {
                    alert('Error al guardar el registro.')
                }
            }
        },
        async loadRecords() {
            try {
                const res = await axios.get(`${process.env.VUE_APP_API_URL}/api/humidity-records`)
                this.recordsAll = res.data  // ya que es un array plano
            } catch (error) {
                console.error("Error al cargar los registros:", error)
            }
        }
        ,
        async fetchLines() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-lines`);
                if (response.status === 200) {
                    this.lines = response.data;
                } else {
                    console.warn("No se pudieron cargar las lineas");
                }
            } catch (error) {
                console.error("Error al obtener las lineas:", error);
            }
        },
        async fetchFormats(lineId) {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-formats/${lineId}`);
                this.formats = response.data;
            } catch (error) {
                console.error("Error al obtener los formatos:", error);
            }
        },
        goToPage(page) {
            this.currentPage = page;
            this.loadRecords();  // Al cambiar de página, recargar los registros
        }
        ,
        previousPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.loadRecords();  // Recargar los registros para la nueva página
            }
        },

        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
                this.loadRecords();  // Recargar los registros para la nueva página
            }
        }
        ,
        resetForm() {
            const now = new Date()
            this.form = {
                balance: '',
                date: now.toISOString().substr(0, 10),
                time: now.toTimeString().substr(0, 5),
                line: '',
                format: '',
                zone: '',
                humidity: '',
                responsible: '',
                observations: ''
            }
        },
        async authenticate() {
            try {
                const response = await axios.post(
                    `${process.env.VUE_APP_API_URL}/api/login-supervisor`,
                    {
                        username: this.username,
                        password: this.password,
                        area: "Calidad", // puedes cambiar esto si necesitas distinguirlo
                    }
                );

                if (response.data.success) {
                    this.errorMessage = "";
                    this.showLoginModal = false;
                    this.downloadHumidityExcel(); // llama a la función de descarga
                } else {
                    this.errorMessage = response.data.message || "Usuario o contraseña incorrectos.";
                }
            } catch (error) {
                this.errorMessage = "Usuario o contraseña incorrectos.";
                console.error("Error en autenticación:", error);
            }
        },

        async downloadHumidityExcel() {
            try {
                const response = await axios.get(
                    `${process.env.VUE_APP_API_URL}/api/download-humidity`,
                    { responseType: "blob" }
                );
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement("a");
                link.href = url;
                link.setAttribute("download", "registro-humedades.xlsx");
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } catch (error) {
                console.error("Error al descargar el archivo Excel:", error);
                alert("Error al descargar el archivo Excel.");
            }
        },
    },
    mounted() {
        this.loadRecords()
        this.fetchLines()
        this.resetForm() // Setear valores por defecto al cargar
    }
}
</script>

<style scoped>
.container {
    max-width: 1600px;
    margin: 0 auto;
    padding: 20px;
}

.card {
    max-width: 1200px;
}

.card-title {
    font-weight: bold;
}

/* Estilo para la tabla */
.table-responsive {
    max-width: 100%;
    overflow-x: auto;
}

/* Barra de paginación */
/* Estilos para la barra de paginación */
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

.card-body input[type="text"],
.card-body textarea {
    text-transform: uppercase;
}



.login-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.modal-dialog {
    width: 100%;
    max-width: 500px;
}

.modal-content {
    background-color: #fff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.lowercase-input {
    text-transform: lowercase;
}
</style>