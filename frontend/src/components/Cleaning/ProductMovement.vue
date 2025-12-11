<template>
    <div class="container mt-5">
        <h2 class="my-4 text-center">Kardex de Limpieza</h2>

        <!-- FORMULARIO DE EGRESOS -->
        <div class="card p-4 mb-5">
            <h4 class="text-center mb-4 text-danger">
                <i class="fas fa-arrow-down"></i> Registro de Egresos
            </h4>

            <form @submit.prevent="submitEgress">
                <div class="row">
                    <div class="form-group col-md-6">
                        <label for="productTypeEgress">Tipo de Producto</label>
                        <select id="productTypeEgress" class="form-control" v-model="egress.selectedType"
                            @change="fetchProducts('egress')">
                            <option value="">Seleccione un tipo</option>
                            <option value="PAPEL">PAPEL</option>
                            <option value="INSECTICIDAS">INSECTICIDAS</option>
                            <option value="JABONES Y DESINFECTANTES">JABONES Y DESINFECTANTES</option>
                            <option value="ESCOBAS Y TRAPEADORES">ESCOBAS Y TRAPEADORES</option>
                            <option value="CEPILLOS ESPECIALES">CEPILLOS ESPECIALES</option>
                        </select>
                    </div>

                    <div class="form-group col-md-6">
                        <label for="productSelectEgress">Seleccionar Producto</label>
                        <select id="productSelectEgress" class="form-control" v-model="egress.selectedProduct" required>
                            <option disabled value="">Seleccione un producto</option>
                            <option v-for="product in egress.products" :key="product.id" :value="product.id">
                                {{ product.name }}
                            </option>
                        </select>
                    </div>
                </div>

                <div class="row mt-3">
                    <div class="form-group col-md-6">
                        <label for="balanceEgress">Saldo Actual</label>
                        <input type="text" id="balanceEgress" class="form-control" v-model="egress.currentBalance"
                            readonly />
                    </div>

                    <div class="form-group col-md-6">
                        <label for="dateEgress">Fecha</label>
                        <input type="date" id="dateEgress" class="form-control" v-model="egress.movementDate"
                            required />
                    </div>
                </div>

                <div class="row mt-3">
                    <div class="form-group col-md-6">
                        <label for="quantityEgress">Cantidad</label>
                        <input type="number" id="quantityEgress" class="form-control" v-model="egress.quantity" required
                            min="1" />
                    </div>

                    <div class="form-group col-md-6">
                        <label for="areaEgress">Área</label>
                        <input type="text" id="areaEgress" class="form-control" v-model="egress.area" required />
                    </div>
                </div>

                <div class="row mt-3">
                    <div class="form-group col-md-6">
                        <label for="responsibleEgress">Responsable</label>
                        <input type="text" id="responsibleEgress" class="form-control" v-model="egress.responsible"
                            required />
                    </div>
                </div>

                <div class="form-group mt-3">
                    <label for="observationsEgress">Observaciones</label>
                    <textarea id="observationsEgress" class="form-control" v-model="egress.observations"
                        rows="3"></textarea>
                </div>

                <div class="d-flex justify-content-between align-items-center mt-4">
                    <div class="flex-grow-1 d-flex justify-content-center">
                        <button type="submit" class="btn btn-danger w-50">
                            <i class="fas fa-save"></i> Registrar
                        </button>
                    </div>
                    <div>
                        <button class="btn btn-secondary" @click="showLoginModal = true">
                            <i class="fas fa-user-lock"></i> 
                        </button>
                    </div>
                </div>

            </form>
        </div>

        <!-- FORMULARIO DE INGRESOS -->
        <div v-if="showIncomeForm" class="card p-4">
            <h4 class="text-center mb-4 text-success">
                <i class="fas fa-arrow-up"></i> Registro de Ingresos
            </h4>

            <form @submit.prevent="submitIncome">
                <div class="row">
                    <div class="form-group col-md-6">
                        <label for="productTypeIncome">Tipo de Producto</label>
                        <select id="productTypeIncome" class="form-control" v-model="income.selectedType"
                            @change="fetchProducts('income')">
                            <option value="">Seleccione un tipo</option>
                            <option value="PAPEL">PAPEL</option>
                            <option value="INSECTICIDAS">INSECTICIDAS</option>
                            <option value="JABONES Y DESINFECTANTES">JABONES Y DESINFECTANTES</option>
                            <option value="ESCOBAS Y TRAPEADORES">ESCOBAS Y TRAPEADORES</option>
                            <option value="CEPILLOS ESPECIALES">CEPILLOS ESPECIALES</option>
                        </select>
                    </div>

                    <div class="form-group col-md-6">
                        <label for="productSelectIncome">Seleccionar Producto</label>
                        <select id="productSelectIncome" class="form-control" v-model="income.selectedProduct" required>
                            <option disabled value="">Seleccione un producto</option>
                            <option v-for="product in income.products" :key="product.id" :value="product.id">
                                {{ product.name }}
                            </option>
                        </select>
                    </div>
                </div>

                <div class="row mt-3">
                    <div class="form-group col-md-6">
                        <label for="balanceIncome">Saldo Actual</label>
                        <input type="text" id="balanceIncome" class="form-control" v-model="income.currentBalance"
                            readonly />
                    </div>

                    <div class="form-group col-md-6">
                        <label for="dateIncome">Fecha</label>
                        <input type="date" id="dateIncome" class="form-control" v-model="income.movementDate"
                            required />
                    </div>
                </div>

                <div class="row mt-3">
                    <div class="form-group col-md-6">
                        <label for="quantityIncome">Cantidad</label>
                        <input type="number" id="quantityIncome" class="form-control" v-model="income.quantity" required
                            min="1" />
                    </div>

                    <div class="form-group col-md-6">
                        <label for="areaIncome">Área</label>
                        <input type="text" id="areaIncome" class="form-control" v-model="income.area" required />
                    </div>
                </div>

                <div class="row mt-3">
                    <div class="form-group col-md-6">
                        <label for="responsibleIncome">Responsable</label>
                        <input type="text" id="responsibleIncome" class="form-control" v-model="income.responsible"
                            required />
                    </div>
                </div>

                <div class="form-group mt-3">
                    <label for="observationsIncome">Observaciones</label>
                    <textarea id="observationsIncome" class="form-control" v-model="income.observations"
                        rows="3"></textarea>
                </div>

                <div class="d-flex justify-content-center mt-4">
                    <button type="submit" class="btn btn-success w-50">
                        <i class="fas fa-save"></i> Registrar Ingreso
                    </button>
                </div>
            </form>
        </div>

        <!-- MODAL LOGIN -->
        <div v-if="showLoginModal" class="modal-overlay">
            <div class="modal-content">
                <h5 class="text-center mb-3">Iniciar Sesión</h5>

                <div class="form-group mb-3">
                    <label>Usuario</label>
                    <input type="text" class="form-control" v-model="username" />
                </div>

                <div class="form-group mb-3">
                    <label>Contraseña</label>
                    <input type="password" class="form-control" v-model="password" />
                </div>

                <p class="text-danger text-center">{{ errorMessage }}</p>

                <div class="d-flex justify-content-between mt-4">
                    <button class="btn btn-primary w-50 me-2" @click="authenticate">
                        Ingresar
                    </button>
                    <button class="btn btn-secondary w-50" @click="showLoginModal = false">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            showIncomeForm: false,
            showLoginModal: false,
            username: "",
            password: "",
            errorMessage: "",
            egress: {
                selectedType: "",
                selectedProduct: "",
                products: [],
                currentBalance: 0,
                movementDate: "",
                quantity: 0,
                area: "",
                responsible: "",
                observations: "",
            },
            income: {
                selectedType: "",
                selectedProduct: "",
                products: [],
                currentBalance: 0,
                movementDate: "",
                quantity: 0,
                area: "",
                responsible: "",
                observations: "",
            },
        };
    },
    watch: {
        "egress.selectedProduct"(newProductId) {
            if (newProductId) this.fetchProductBalance(newProductId, "egress");
        },
        "income.selectedProduct"(newProductId) {
            if (newProductId) this.fetchProductBalance(newProductId, "income");
        },
    },
    methods: {
        async fetchProducts(type) {
            try {
                const target = this[type];
                if (!target.selectedType) {
                    target.products = [];
                    return;
                }
                const response = await axios.get(
                    `${process.env.VUE_APP_API_URL}/api/cleaning-products`,
                    { params: { type: target.selectedType } }
                );
                target.products = response.data;
            } catch (error) {
                console.error("Error al cargar productos:", error);
            }
        },

        async fetchProductBalance(productId, type) {
            try {
                const response = await axios.get(
                    `${process.env.VUE_APP_API_URL}/api/product-balance/${productId}`
                );
                this[type].currentBalance = response.data.quantity;
            } catch (error) {
                console.error("Error al obtener saldo:", error);
            }
        },

        async submitEgress() {
            await this.submitMovement("egress", "Egreso registrado exitosamente");
        },
        async submitIncome() {
            await this.submitMovement("income", "Ingreso registrado exitosamente");
        },

        async submitMovement(type, successMsg) {
            try {
                const form = this[type];
                const data = {
                    product_id: form.selectedProduct,
                    date: form.movementDate,
                    area: form.area.toUpperCase(),
                    income: type === "income" ? form.quantity : 0,
                    outcome: type === "egress" ? form.quantity : 0,
                    responsible: form.responsible.toUpperCase(),
                    observations: form.observations.toUpperCase(),
                };
                await axios.post(`${process.env.VUE_APP_API_URL}/api/register-movement`, data);
                alert(successMsg);
                this.resetForm(type);
            } catch (error) {
                alert("Error al registrar el movimiento");
                console.error(error);
            }
        },

        async authenticate() {
            try {
                const response = await axios.post(
                    `${process.env.VUE_APP_API_URL}/api/login-supervisor`,
                    {
                        username: this.username,
                        password: this.password,
                        area: "Limpieza",
                    }
                );
                if (response.data.success) {
                    this.errorMessage = "";
                    this.showLoginModal = false;
                    this.showIncomeForm = true;
                    alert(response.data.message);
                } else {
                    this.errorMessage = response.data.message;
                }
            } catch {
                this.errorMessage = "Usuario o contraseña incorrectos.";
            }
        },

        resetForm(type) {
            Object.keys(this[type]).forEach((key) => (this[type][key] = ""));
            this[type].currentBalance = 0;
        },
    },
};
</script>

<style scoped>
.card {
    max-width: 900px;
    margin: 0 auto;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-content {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    width: 400px;
}

label {
    font-weight: bold;
}

input[type="text"],
textarea {
    text-transform: uppercase;
}
</style>
