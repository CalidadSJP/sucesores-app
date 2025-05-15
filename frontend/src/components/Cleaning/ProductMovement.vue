<template>
    <div class="container mt-5">
        <h2 class="my-4 text-center">Registro de Ingreso / Egreso de Producto</h2>

        <div class="card p-4">
            <form @submit.prevent="submitForm">
                <div class="row">
                    <!-- Tipo de producto -->
                    <div class="form-group col-md-6">
                        <label for="productType">Tipo de Producto</label>
                        <select id="productType" class="form-control" v-model="selectedType" @change="fetchProducts">
                            <option value="">Seleccione un tipo</option>
                            <option value="PAPEL">PAPEL</option>
                            <option value="INSECTICIDAS">INSECTICIDAS</option>
                            <option value="JABONES Y DESINFECTANTES">JABONES Y DESINFECTANTES</option>
                            <option value="ESCOBAS Y TRAPEADORES">ESCOBAS Y TRAPEADORES</option>
                        </select>
                    </div><br><br><br>
                    <!-- Producto -->
                    <div class="form-group col-md-6">
                        <label for="productSelect">Seleccionar Producto</label>
                        <select id="productSelect" class="form-control" v-model="selectedProduct" required>
                            <option disabled value="">Seleccione un producto</option>
                            <option v-for="product in products" :key="product.id" :value="product.id">
                                {{ product.name }}
                            </option>
                        </select>
                    </div><br><br><br>
                </div>

                <div class="row">
                    <!-- Saldo actual -->
                    <div class="form-group col-md-6">
                        <label for="currentBalance">Saldo Actual</label>
                        <input type="text" id="currentBalance" class="form-control" v-model="currentBalance" readonly />
                    </div><br><br><br>
                    <!-- Fecha -->
                    <div class="form-group col-md-6">
                        <label for="movementDate">Fecha</label>
                        <input type="date" id="movementDate" class="form-control" v-model="movementDate" required />
                    </div><br><br><br>
                </div>

                <div class="row">
                    <!-- Tipo -->
                    <div class="form-group col-md-6">
                        <label for="movementType">Tipo de Movimiento</label>
                        <select id="movementType" class="form-control" v-model="movementType" required>
                            <option value="Ingreso">Ingreso</option>
                            <option value="Egreso">Egreso</option>
                        </select>
                    </div><br><br><br>
                    <!-- Cantidad -->
                    <div class="form-group col-md-6">
                        <label for="quantity">Cantidad</label>
                        <input type="number" id="quantity" class="form-control" v-model="quantity" required min="1" />
                    </div><br><br><br>
                </div>

                <div class="row">
                    <!-- Área -->
                    <div class="form-group col-md-6">
                        <label for="area">Área</label>
                        <input type="text" id="area" class="form-control" v-model="area" required />
                    </div><br><br><br>

                    <!-- Área -->
                    <div class="form-group col-md-6">
                        <label for="reponsible">Responsable</label>
                        <input type="text" id="reponsible" class="form-control" v-model="responsible" required />
                    </div><br><br><br>
                </div>

                <!-- Observaciones -->
                <div class="form-group">
                    <label for="observations">Observaciones</label>
                    <textarea id="observations" class="form-control" v-model="observations" rows="3"></textarea>
                </div><br>

                <div class="d-flex flex-wrap">
                    <button type="submit" class="btn btn-primary mb-2 me-2">
                        <i class="fas fa-save"></i> Registrar
                    </button>
                    <button class="btn btn-success mb-2" @click="downloadExcel">
                        <i class="fas fa-file-excel"></i> Descargar Registro
                    </button>
                </div>


            </form>
        </div><br><br>
    </div>
</template>


<script>
import axios from 'axios';

export default {
    data() {
        return {
            selectedType: '',
            selectedProduct: '',
            products: [],
            currentBalance: 0,
            movementDate: '',
            movementType: 'Ingreso',
            quantity: 0,
            area: '',
            responsible: '',
            observations: '',
        };
    },
    created() {
        this.fetchProducts();
    },
    watch: {
        selectedProduct(newProductId) {
            if (newProductId) {
                this.fetchProductBalance(newProductId);
            }
        },
    },
    methods: {
        async fetchProducts() {
            try {
                if (!this.selectedType) {
                    this.products = [];
                    return;
                }
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/cleaning-products`, {
                    params: { type: this.selectedType }
                });
                this.products = response.data;
                this.selectedProduct = '';
            } catch (error) {
                console.error('Error al cargar los productos:', error);
            }
        },
        async fetchProductBalance(productId) {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/product-balance/${productId}`);
                this.currentBalance = response.data.quantity;
            } catch (error) {
                console.error('Error al obtener el saldo del producto:', error);
            }
        },
        async submitForm() {
            const movementData = {
                product_id: this.selectedProduct,
                date: this.movementDate,
                area: this.area.toUpperCase(),
                income: this.movementType === 'Ingreso' ? this.quantity : 0,
                outcome: this.movementType === 'Egreso' ? this.quantity : 0,
                responsible: this.responsible.toUpperCase(),
                observations: this.observations.toUpperCase(),
            };

            try {
                await axios.post(`${process.env.VUE_APP_API_URL}/api/register-movement`, movementData);

                // Si llegamos aquí, la petición fue exitosa (status 200–299)
                alert('Movimiento registrado exitosamente');
                this.resetForm();
            } catch (error) {
                // Verificamos si hay mensaje de error del servidor
                if (error.response?.data?.error) {
                    alert('Error: ' + error.response.data.error);
                } else {
                    alert('Error desconocido al registrar el movimiento');
                }
                console.error('Error al registrar el movimiento:', error);
            }
        },
        downloadExcel() {
            const url = `${process.env.VUE_APP_API_URL}/api/download-cleaning-movements`;
            window.open(url, '_blank');
        },

        resetForm() {
            this.selectedType = '';
            this.selectedProduct = '';
            this.currentBalance = 0;
            this.movementDate = '';
            this.movementType = 'Ingreso';
            this.quantity = 0;
            this.area = '';
            this.responsible = '';
            this.observations = '';
        }
    },
};
</script>

<style scoped>
.card {
    max-width: 900px;
    margin: 0 auto;
}

label {
    font-weight: bold;
}

input[type="text"],
textarea {
    text-transform: uppercase;
}
</style>