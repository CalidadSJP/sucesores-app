<template>
    <div class="container mt-4">
        <!-- Tarjeta 1: Datos generales -->
        <div class="card">
            <div class="card-header text-center">
                <h3>Datos</h3>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6" v-for="key in generalKeys" :key="key">
                        <label class="form-label">{{ formatLabel(key) }}</label>
                        <input type="text" class="form-control" :value="formatValue(key, weightData[key])" disabled />
                    </div>
                </div>
            </div>
        </div>
        <div class="card mt-4">
            <div class="card-header text-center">
                <h3>Pesos Registrados</h3>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-2" v-for="(weight, index) in weights" :key="index">
                        <label class="form-label">P{{ index + 1 }}</label>
                        <input type="text" class="form-control text-center" :value="weight" disabled />
                    </div>
                </div>
            </div>
        </div>
        <!-- Tarjeta 2: Estadísticas de peso -->
        <div class="card mt-4">
            <div class="card-header text-center">
                <h3>Resultados</h3>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6" v-for="key in statsKeys" :key="key">
                        <label class="form-label">{{ formatLabel(key) }}</label>
                        <input type="text" class="form-control" :value="formatValue(key, weightData[key])" disabled />
                    </div>
                </div>
            </div>
        </div>
        <!-- Gráfico de dispersión -->
        <div class="card mt-4">
            <div class="card-body">
                <h4 class="text-center">Dispersión de Pesos</h4>
                <Scatter id="weight-scatter" :data="chartData" :options="chartOptions" />
            </div>
        </div><br><br>
    </div>
</template>

<script>
import axios from "axios";
import { Scatter } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, Legend, PointElement, LineElement, LinearScale, LineController } from "chart.js";
import ChartAnnotation from 'chartjs-plugin-annotation'; // Elimina esta línea

// Registrar Chart.js
ChartJS.register(Title, Tooltip, Legend, PointElement, LineElement, LinearScale, LineController, ChartAnnotation);

export default {
    components: { Scatter },
    data() {
        return {
            weightData: {},
            weightPoints: [], // Pesos individuales
            weights: [],
            limiteMax: null,
            limiteMin: null,
            net_weight: null,
            avg: null,
            generalKeys: [
                "date", "baler", "net_weight", "format", "brand", "lot",
                "ean13", "manufacture_date", "expiry_date"
            ],
            statsKeys: [
                "average", "minimum", "maximum", "standard_deviation", "count_t1",
                "count_t2", "limite_maximo_operativo", "limite_minimo_operativo", "result"
            ],
        };
    },
    computed: {
        chartData() {
            return {
                datasets: [
                    {
                        label: "Peso Registrado",
                        data: this.weightPoints,
                        backgroundColor: "blue",
                        pointRadius: 5,
                        type: "line",
                        borderColor: "rgb(152, 210, 255)",
                    },
                    {
                        label: "Peso Promedio",
                        data: this.weightPoints.map((p) => ({ x: p.x, y: this.avg })),
                        borderColor: "green",
                        borderDash: [5, 5], // Línea punteada
                        borderWidth: 2,
                        fill: false,
                        type: "line",
                        pointRadius: 0,  // Eliminar puntos
                    },
                    {
                        label: "Peso Neto",
                        data: this.weightPoints.map((p) => ({ x: p.x, y: this.net_weight })),
                        borderColor: "purple",
                        borderWidth: 2,
                        fill: false,
                        type: "line",
                        pointRadius: 0,  // Eliminar puntos
                    },
                    {
                        label: "Límite Mínimo Normativo",
                        data: this.weightPoints.map((p) => ({ x: p.x, y: this.limiteMin })),
                        borderColor: "red",
                        borderWidth: 2,
                        fill: false,
                        type: "line",
                        pointRadius: 0,  // Eliminar puntos
                    },
                    {
                        label: "Límite Máximo Normativo",
                        data: this.weightPoints.map((p) => ({ x: p.x, y: this.limiteMax })),
                        borderColor: "orange",
                        borderWidth: 2,
                        fill: false,
                        type: "line",
                        pointRadius: 0,  // Eliminar puntos
                    },
                ],
            };
        },
        chartOptions() {
            // Calcular el límite superior e inferior del eje Y basándonos en el peso neto y los límites operativos
            const netWeight = this.weightData.net_weight;
            const limiteMax = this.weightData.limite_maximo_operativo;
            const limiteMin = this.weightData.limite_minimo_operativo;
            const margin = 5; // Margen adicional alrededor del peso neto y límites operativos

            // Calcular los límites del eje Y considerando el máximo y mínimo del peso neto, y los límites operativos
            const minY = Math.min(netWeight, limiteMin) - margin;
            const maxY = Math.max(netWeight, limiteMax) + margin;

            return {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "top",
                    },
                    annotation: {  // Aquí añadimos la configuración para las anotaciones
                        annotations: {
                            averageWeight: {
                                type: 'label',
                                // Ajustamos xMin y xMax para que estén al final de la línea
                                xMin: this.weightPoints.length,  // Coloca la anotación al final de la línea
                                xMax: this.weightPoints.length + 3,  // Mantiene la posición X al final
                                yMin: this.avg,   // Establecemos el valor en el eje Y para mostrar el promedio
                                yMax: this.avg,
                                backgroundColor: 'green',
                                content: `${this.avg}`, // Contenido de la anotación (el valor promedio)
                                font: {
                                    size: 12,
                                    weight: 'bold',
                                },
                                color: 'black', // Color del texto
                                textAlign: 'center',
                                textBaseline: 'middle',
                            },
                            netWeight: {
                                type: 'label',
                                // Ajustamos xMin y xMax para que estén al final de la línea
                                xMin: this.weightPoints.length,  // Coloca la anotación al final de la línea
                                xMax: this.weightPoints.length + 3,  // Mantiene la posición X al final
                                yMin: this.net_weight,   // Establecemos el valor en el eje Y para mostrar el promedio
                                yMax: this.net_weight,
                                backgroundColor: 'purple',
                                content: `${this.net_weight}`, // Contenido de la anotación (el valor promedio)
                                font: {
                                    size: 12,
                                    weight: 'bold',
                                },
                                color: 'black', // Color del texto
                                textAlign: 'center',
                                textBaseline: 'middle',
                            },
                            limiteMinOperativo: {
                                type: 'label',
                                xMin: this.weightPoints.length, // Coloca la anotación al final de la línea
                                xMax: this.weightPoints.length + 3, // Ajusta la posición X al final
                                yMin: this.limiteMin,   // Establecemos el valor en el eje Y para mostrar el límite mínimo operativo
                                yMax: this.limiteMin,
                                backgroundColor: 'red',
                                content: `${this.limiteMin}`, // Contenido de la anotación (el límite mínimo operativo)
                                font: {
                                    size: 12,
                                    weight: 'bold',
                                },
                                color: 'black', // Color del texto
                                textAlign: 'center',
                                textBaseline: 'middle',
                            },
                            limiteMaxOperativo: {
                                type: 'label',
                                xMin: this.weightPoints.length, // Coloca la anotación al final de la línea
                                xMax: this.weightPoints.length + 3, // Ajusta la posición X al final
                                yMin: this.limiteMax,   // Establecemos el valor en el eje Y para mostrar el límite máximo operativo
                                yMax: this.limiteMax,
                                backgroundColor: 'orange',
                                content: `${this.limiteMax}`, // Contenido de la anotación (el límite máximo operativo)
                                font: {
                                    size: 12,
                                    weight: 'bold',
                                },
                                color: 'black', // Color del texto
                                textAlign: 'center',
                                textBaseline: 'middle',
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        type: "linear",
                        position: "bottom",
                        title: { display: true, text: "Muestras" },
                        min: 0, // Límite mínimo para X (ajustar según sea necesario)
                        max: this.weightPoints.length + 3, // El número de puntos de datos
                    },
                    y: {
                        title: { display: true, text: "Peso" },
                        min: minY, // Límite mínimo para Y basado en el peso neto
                        max: maxY, // Límite máximo para Y basado en el peso neto
                    },
                },
            };
        },
    },
    methods: {
        async fetchWeightData() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-last-weight-summary`);
                this.weightData = response.data;

                // Obtener datos históricos para el gráfico
                const historyResponse = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-weight-history`);

                this.weightPoints = historyResponse.data.weights;
                this.limiteMax = historyResponse.data.limite_maximo_operativo;
                this.limiteMin = historyResponse.data.limite_minimo_operativo;
                this.net_weight = historyResponse.data.net_weight;
                this.avg = historyResponse.data.average;
            } catch (error) {
                console.error("Error obteniendo los datos:", error);
            }
        },
        async fetchWeights() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/get-last-weights`);
                this.weights = response.data.weights;
            } catch (error) {
                console.error("Error obteniendo los últimos pesos registrados:", error);
            }
        },
        formatLabel(key) {
            const labels = {
                date: "Fecha",
                baler: "Empacadora",
                net_weight: "Peso Neto",
                format: "Formato",
                brand: "Marca",
                lot: "Lote",
                ean13: "EAN 13",
                manufacture_date: "Fecha de Fabricación",
                expiry_date: "Fecha de Expiración",
                average: "Peso Promedio",
                minimum: "Peso Mínimo",
                maximum: "Peso Máximo",
                standard_deviation: "Desviación Estándar",
                count_t1: "Errores T1",
                count_t2: "Errores T2",
                limite_maximo_operativo: "Límite Máximo Normativo",
                limite_minimo_operativo: "Límite Mínimo Normativo",
                result: "Resultado",
            };
            return labels[key] || key;
        },
        formatValue(key, value) {
            if (["date", "manufacture_date", "expiry_date"].includes(key) && value) {
                return new Date(value).toLocaleDateString("es-ES", {
                    day: "2-digit",
                    month: "2-digit",
                    year: "numeric",
                });
            }
            return value;
        },
    },
    mounted() {
        this.fetchWeightData();
        this.fetchWeights();
    },
};
</script>

<style>
.card {
    max-width: 800px;
    margin: auto;
}

.form-control {
    background-color: #f8f9fa;
    font-weight: bold;
}


/* Establecer altura fija para el gráfico */
#weight-scatter {
    height: 300px;
    /* Ajusta el valor a lo que necesites */
    width: 100%;
    max-height: 400px;
    /* Para no dejarlo demasiado grande */
}
</style>
