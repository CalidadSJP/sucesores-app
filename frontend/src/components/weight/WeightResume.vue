<template>
    <div class="container mt-4">
        <!-- Resumen de Control de Pesos -->
        <div class="card">
            <div class="card-header text-center">
                <h3>Resumen de Control de Pesos</h3>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6" v-for="key in orderedKeys" :key="key">
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

// Registrar Chart.js
ChartJS.register(Title, Tooltip, Legend, PointElement, LineElement, LinearScale, LineController);

export default {
    components: { Scatter },
    data() {
        return {
            weightData: {},
            weightPoints: [], // Pesos individuales
            limiteMax: null,
            limiteMin: null,
            avg: null,
            orderedKeys: [
                "date",
                "baler",
                "net_weight",
                "format",
                "brand",
                "lot",
                "manufacture_date",
                "expiry_date",
                "average",
                "minimum",
                "maximum",
                "standard_deviation",
                "count_t1",
                "count_t2",
                "limite_maximo_operativo",
                "limite_minimo_operativo",
                "result",
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
                        label: "Límite Mínimo Operativo",
                        data: this.weightPoints.map((p) => ({ x: p.x, y: this.limiteMin })),
                        borderColor: "red",
                        borderWidth: 2,
                        fill: false,
                        type: "line",
                        pointRadius: 0,  // Eliminar puntos
                    },
                    {
                        label: "Límite Máximo Operativo",
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
                },
                scales: {
                    x: {
                        type: "linear",
                        position: "bottom",
                        title: { display: true, text: "Muestras" },
                        min: 0, // Límite mínimo para X (ajustar según sea necesario)
                        max: this.weightPoints.length + 1, // El número de puntos de datos

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
                this.avg = historyResponse.data.average;
            } catch (error) {
                console.error("Error obteniendo los datos:", error);
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
                manufacture_date: "Fecha de Fabricación",
                expiry_date: "Fecha de Expiración",
                average: "Peso Promedio",
                minimum: "Peso Mínimo",
                maximum: "Peso Máximo",
                standard_deviation: "Desviación Estándar",
                count_t1: "Errores T1",
                count_t2: "Errores T2",
                limite_maximo_operativo: "Límite Máximo Operativo",
                limite_minimo_operativo: "Límite Mínimo Operativo",
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
