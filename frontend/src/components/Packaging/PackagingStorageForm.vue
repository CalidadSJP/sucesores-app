<template>
    <div class="container mt-4">
        <h1 class="text-center mb-4">Ingreso de Material de Empaque</h1>
        <form @submit.prevent="submitForm" enctype="multipart/form-data">

            <!-- TRANSPORTE -->
            <div class="card mb-4">
                <div class="card-header custom-header bg-primary text-white">
                    <h3 class="m-0">Transporte</h3>
                    <button @click="$router.push('/additive-home')" class="btn btn-primary custom-back-button">
                        <img src="@/assets/back-arrow.png" alt="Regresar" class="button-icon" />
                        <span class="button-text">Regresar</span>
                    </button>
                </div>
                <div class="card-body">
                    <!-- Fecha Actual -->
                    <div class="mb-3">
                        <label for="entryDate" class="form-label">Fecha</label>
                        <input type="date" class="form-control" id="entryDate" v-model="form.entry_date" required>
                    </div>

                    <!-- Proveedor -->
                    <div class="mb-3">
                        <label for="supplier" class="form-label">Proveedor</label>
                        <select class="form-select" id="supplier" v-model="form.supplier" required>
                            <option value="" disabled>Seleccione...</option>
                            <option v-for="supplier in suppliers" :key="supplier" :value="supplier">
                                {{ supplier }}
                            </option>
                        </select>
                    </div><br>

                    <!-- DOCUMENTOS -->
                    <h4 class="mt-4">Documentos</h4><br>

                    <!-- Nombre del chofer -->
                    <div class="mb-3">
                        <label for="driverName" class="form-label">Nombre del chofer</label>
                        <input type="text" class="form-control" id="driverName"
                            @input="convertToUppercase('driver_name')" v-model="form.driver_name">
                    </div>

                    <!-- No. de cédula del chofer -->
                    <div class="mb-3">
                        <label for="driverId" class="form-label">No. de cédula del chofer</label>
                        <input type="text" class="form-control" id="driverId" v-model="form.driver_id">
                    </div>

                    <!-- Permiso de Transporte de Alimentos -->
                    <div class="mb-3">
                        <label for="foodTransportPermission" class="form-label">Permiso de Transporte de
                            Alimentos</label>
                        <select class="form-select" id="foodTransportPermission"
                            v-model="form.food_transport_permission">
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                            <option value="NO_APLICA">NO APLICA</option>
                        </select>
                    </div>

                    <!-- Validez del permiso de transporte -->
                    <div class="mb-3">
                        <label for="foodTransportValidity" class="form-label">Validez del Permiso de Transporte</label>
                        <input type="text" class="form-control" id="foodTransportValidity"
                            @input="convertToUppercase('food_transport_validity')"
                            v-model="form.food_transport_validity">
                    </div>

                    <!-- Registro de Fumigación -->
                    <div class="mb-3">
                        <label for="fumigationRecord" class="form-label">Registro de Fumigación</label>
                        <select class="form-select" id="fumigationRecord" v-model="form.fumigation_record">
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                            <option value="NO_APLICA">NO APLICA</option>
                        </select>
                    </div>

                    <!-- Última fecha de fumigación -->
                    <div class="mb-3">
                        <label for="lastFumigationDate" class="form-label">Última Fumigación</label>
                        <input type="date" class="form-control" id="lastFumigationDate"
                            v-model="form.last_fumigation_date">
                    </div>

                    <!-- Número de factura -->
                    <div class="mb-3">
                        <label for="invoiceNumber" class="form-label">Número de factura/guía de remisión</label>
                        <input type="text" class="form-control" id="invoiceNumber"
                            @input="convertToUppercase('invoice_number')" v-model="form.invoice_number">
                    </div>


                    <div class="mb-3">
                        <label class="form-label">Factura/Guía de remisión</label>
                        <select class="form-select" v-model="form.invoice_file_confirmation">
                            <option value="">Selecciona una opción</option>
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>

                        <!-- Campo de subir archivo si el usuario selecciona "Sí" -->
                        <div v-if="form.invoice_file_confirmation === 'SI'" class="mt-2">
                            <label for="invoiceFile" class="form-label">Factura/Guía de remisión</label>
                            <input type="file" class="form-control" id="invoiceFile" ref="invoiceFile"
                                @change="handleFileUpload('invoice_file', $event)">
                        </div>
                    </div><br>

                    <!-- ESTADO DEL CAMIÓN -->
                    <h4 class="mt-4">Estado del Camión</h4><br>

                    <!-- Olores extraños -->
                    <div class="mb-3">
                        <label for="strangeSmells" class="form-label">Olores extraños</label>
                        <select class="form-select" id="strangeSmells" v-model="form.strange_smells">
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>
                    </div>

                    <!-- Evidencia de plagas -->
                    <div class="mb-3">
                        <label for="pestsEvidence" class="form-label">Evidencia de plagas</label>
                        <select class="form-select" id="pestsEvidence" v-model="form.pests_evidence">
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>
                    </div>

                    <!-- Camión limpio -->
                    <div class="mb-3">
                        <label for="cleanTruck" class="form-label">Camión limpio</label>
                        <select class="form-select" id="cleanTruck" v-model="form.clean_truck">
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>
                    </div>

                    <!-- Personal uniformado -->
                    <div class="mb-3">
                        <label for="uniformedPersonnel" class="form-label">Personal uniformado y limpio</label>
                        <select class="form-select" id="uniformedPersonnel" v-model="form.uniformed_personnel">
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>
                    </div>

                    <!-- Estado de piso, paredes y techo -->
                    <div class="mb-3">
                        <label for="floorWallsRoofCondition" class="form-label">Estado de piso, paredes y techo</label>
                        <select class="form-select" id="floorWallsRoofCondition"
                            v-model="form.floor_walls_roof_condition">
                            <option value="BIEN">Bien</option>
                            <option value="MAL">Mal</option>
                        </select>
                    </div>

                    <!-- Huecos en la caja del camión -->
                    <div class="mb-3">
                        <label for="truckBoxHoles" class="form-label">Agujeros en cajón</label>
                        <select class="form-select" id="truckBoxHoles" v-model="form.truck_box_holes">
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>
                    </div>

                    <!-- Sticker de desinfección -->
                    <div class="mb-3">
                        <label for="disinfectionSticker" class="form-label">Sticker de desinfección</label>
                        <select class="form-select" id="disinfectionSticker" v-model="form.disinfection_sticker">
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>
                    </div>

                    <!-- Confirmación y Archivo: Truck Condition Image -->
                    <div class="mb-3">
                        <label class="form-label">Imagen de condición del camión</label>
                        <select class="form-select" v-model="form.truck_condition_image_confirmation">
                            <option value="">Selecciona una opción</option>
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>

                        <div v-if="form.truck_condition_image_confirmation === 'SI'" class="mt-2">
                            <label for="truckConditionImage" class="form-label">Imagen de Condición del Camión</label>
                            <input type="file" class="form-control" id="truckConditionImage" ref="truckConditionImage"
                                @change="handleFileUpload('truck_condition_image', $event)">
                        </div>
                    </div>

                    <!-- Confirmación y Archivo: Truck Plate Image -->
                    <div class="mb-3">
                        <label class="form-label">Imagen de la Placa del Camión</label>
                        <select class="form-select" v-model="form.truck_plate_image_confirmation">
                            <option value="">Selecciona una opción</option>
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>

                        <div v-if="form.truck_plate_image_confirmation === 'SI'" class="mt-2">
                            <label for="truckPlateImage" class="form-label">Imagen de Placa del Camión</label>
                            <input type="file" class="form-control" id="truckPlateImage" ref="truckPlateImage"
                                @change="handleFileUpload('truck_plate_image', $event)">
                        </div>
                    </div> 


                    <button type="button" class="btn btn-secondary mt-3" @click="clearTransportFields">Limpiar
                        Transporte</button>
                </div>
            </div>

            <!-- PRODUCTO -->
            <div class="card mb-4">
                <div class="card-header bg-success text-white">
                    <h3 class="m-0">Producto</h3>
                </div>
                <div class="card-body">


                    <!-- Marca -->
                    <div class="mb-3">
                        <label for="brand" class="form-label">Marca</label>
                        <select class="form-select" id="brand" v-model="form.brand" required>
                            <option value="" disabled>Seleccione...</option>
                            <option v-for="brand in brands" :key="brand" :value="brand">
                                {{ brand }}
                            </option>
                        </select>
                    </div>

                    <!-- Producto -->
                    <div class="mb-3">
                        <label for="product" class="form-label">Producto</label>
                        <select class="form-select" id="product" v-model="form.product" required>
                            <option value="" disabled>Seleccione...</option>
                            <option v-for="product in products" :key="product" :value="product">
                                {{ product }}
                            </option>
                        </select>
                    </div>

                    <!-- Número de Lote -->
                    <div class="mb-3">
                        <label for="lotNumber" class="form-label">Lote</label>
                        <input type="text" class="form-control" id="lotNumber" v-model="form.lot_number" required>
                    </div>

                    <!-- Cantidad de paquetes -->
                    <div class="mb-3">
                        <label for="packageQuantity" class="form-label">Cantidad de bultos</label>
                        <input type="number" class="form-control" id="packageQuantity" v-model="form.package_quantity"
                            required>
                    </div>

                    <!-- Peso Total -->
                    <div class="mb-3">
                        <label for="totalWeight" class="form-label">Cantidad total (Kg/Sobres)</label>
                        <input type="number" placeholder="1.0" step="0.01" min="0" max="1000" class="form-control"
                            id="totalWeight" v-model="form.total_weight" required>
                    </div>

                    <!-- Fecha de fabricación -->
                    <div class="mb-3">
                        <label for="manufactureDate" class="form-label">Fecha de fabricación</label>
                        <input type="date" class="form-control" id="manufactureDate" v-model="form.manufacture_date"
                            required>
                    </div>

                    <!-- Fecha de caducidad -->
                    <div class="mb-3">
                        <label for="expiryDate" class="form-label">Fecha de caducidad</label>
                        <input type="date" class="form-control" id="expiryDate" v-model="form.expiry_date" required>
                    </div>

                    <!-- Confirmación y Archivo: Technical File -->
                    <div class="mb-3">
                        <label class="form-label">Ficha Técnica/Certificado de Calidad</label>
                        <select class="form-select" v-model="form.technical_file_confirmation">
                            <option value="">Selecciona una opción</option>
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>

                        <div v-if="form.technical_file_confirmation === 'SI'" class="mt-2">
                            <label for="technicalFile" class="form-label">Ficha Técnica/Certificado de Calidad</label>
                            <input type="file" class="form-control" ref="technicalFile" id="technicalFile"
                                @change="handleFileUpload('technical_file', $event)">
                        </div>
                    </div>




                    <!-- ESTADO DEL PRODUCTO -->
                    <h4 class="mt-4">Estado del Producto</h4><br>

                    <!-- Cuerpos extraños -->
                    <div class="mb-3">
                        <label for="foreignBodies" class="form-label">Cuerpos extraños</label>
                        <select class="form-select" id="foreignBodies" v-model="form.foreign_bodies">
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>
                    </div>

                    <!-- Fecha de revisión de vida útil -->
                    <div class="mb-3">
                        <label for="shelfLifeCheck" class="form-label">El producto tiene por lo menos 6 meses de vida
                            útil?</label>
                        <select class="form-select" id="shelfLifeCheck" v-model="form.shelf_life_check" required>
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>
                    </div>

                    <!-- Declaración de alérgenos -->
                    <div class="mb-3">
                        <label for="allergenStatement" class="form-label">Declaración de alérgenos</label>
                        <select class="form-select" id="allergenStatement" v-model="form.allergen_statement" required>
                            <option value="CUMPLE">CUMPLE</option>
                            <option value="NO CUMPLE">NO CUMPLE</option>
                            <option value="NO APLICA">NO APLICA</option>
                        </select>
                    </div>

                    <!-- Sistema Gráfico -->
                    <div class="mb-3">
                        <label for="graphicSystem" class="form-label">Sistema Gráfico</label>
                        <select class="form-select" id="graphicSystem" v-model="form.graphic_system" required>
                            <option value="CUMPLE">CUMPLE</option>
                            <option value="NO CUMPLE">NO CUMPLE</option>
                            <option value="NO APLICA">NO APLICA</option>
                        </select>
                    </div>

                    <!-- Producto aceptado -->
                    <div class="mb-3">
                        <label for="productAccepted" class="form-label">Se ACEPTA el producto luego de la inspección
                            visual
                            (producto íntegro y bien codificado)</label>
                        <select class="form-select" id="productAccepted" v-model="form.product_accepted" required>
                            <option value="SI">SI</option>
                            <option value="NO">NO</option>
                        </select>
                    </div>

                    <!-- Razones de rechazo -->
                    <div class="mb-3">
                        <label for="rejectionReasons" class="form-label">En caso de que la respuesta sea no, especifique
                            las razones
                            por las que no se recibió el producto </label>
                        <textarea class="form-control" id="rejectionReasons"
                            @input="convertToUppercase('rejection_reasons')"
                            v-model="form.rejection_reasons"></textarea>
                    </div>

                    <!-- Recibido por -->
                    <div class="mb-3">
                        <label for="receivedBy" class="form-label">Recibido por</label>
                        <input type="text" class="form-control" id="receivedBy"
                            @input="convertToUppercase('received_by')" v-model="form.received_by" required>
                    </div>

                    <button type="button" class="btn btn-secondary mt-3" @click="clearProductFields">Limpiar
                        Producto</button>
                </div>
                <div class="card-footer"><br>
                    <div class="d-flex justify-content-end gap-2">
                        <button type="submit" class="btn btn-primary">Enviar Formulario</button>
                        <button type="button" class="btn btn-secondary" @click="submitFiles">Enviar Archivos</button>
                    </div><br>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            form: {
                entry_date: '',
                supplier: '',
                driver_name: '',
                driver_id: '',
                food_transport_permission: '',
                food_transport_validity: '',
                fumigation_record: '',
                last_fumigation_date: '',
                invoice_number: '',
                invoice_file: null,
                strange_smells: '',
                pests_evidence: '',
                clean_truck: '',
                uniformed_personnel: '',
                floor_walls_roof_condition: '',
                truck_box_holes: '',
                disinfection_sticker: '',
                truck_condition_image: null,
                truck_plate_image: null,
                foreign_bodies: '',
                brand: '',
                product: '',
                lot_number: '',
                technical_file: null,
                package_quantity: '',
                total_weight: '',
                manufacture_date: '',
                expiry_date: '',
                shelf_life_check: '',
                allergen_statement: '',
                graphic_system: '',
                product_accepted: '',
                rejection_reasons: '',
                received_by: '',
                invoice_file_confirmation: '',
                truck_condition_image_confirmation: '',
                truck_plate_image_confirmation: '',
                technical_file_confirmation: '',
            },
            suppliers: [], // Aquí se almacenarán los proveedores
            products: [], // Aquí se almacenarán los productos
            brands:[]
        };
    },
    mounted() {
        this.fetchSuppliers();
        this.fetchProducts();
        this.fetchBrands();
    },
    methods: {
        clearTransportFields() {
            this.form.entry_date = '';
            this.form.supplier = '';
            this.form.driver_name = '';
            this.form.driver_id = '';
            this.form.food_transport_permission = '';
            this.form.food_transport_validity = '';
            this.form.fumigation_record = '';
            this.form.last_fumigation_date = '';
            this.form.invoice_number = '';
            this.form.strange_smells = '';
            this.form.pests_evidence = '';
            this.form.clean_truck = '';
            this.form.uniformed_personnel = '';
            this.form.floor_walls_roof_condition = '';
            this.form.truck_box_holes = '';
            this.form.disinfection_sticker = '';
            if (this.$refs.invoiceFile) this.$refs.invoiceFile.value = null;
            if (this.$refs.truckConditionImage) this.$refs.truckConditionImage.value = null;
            if (this.$refs.truckPlateImage) this.$refs.truckPlateImage.value = null;
        },
        clearProductFields() {
            this.form.product = '';
            this.form.foreign_bodies = '';
            this.form.lot_number = '';
            this.form.technical_file = null;
            this.form.package_quantity = '';
            this.form.total_weight = '';
            this.form.manufacture_date = '';
            this.form.expiry_date = '';
            this.form.shelf_life_check = '';
            this.form.allergen_statement = '';
            this.form.graphic_system = '';
            this.form.product_accepted = '';
            this.form.rejection_reasons = '';
            this.form.received_by = '';
            this.form.brand ='';

            if (this.$refs.technicalFile) this.$refs.technicalFile.value = null;

        },
        handleFileUpload(field, event) {
            const file = event.target.files[0];
            if (file) {
                this.form[field] = file;
            }
        },
        clearFileInputs() {
            // Reiniciar valores del formulario
            this.form.invoice_file = null;
            this.form.truck_condition_image = null;
            this.form.truck_plate_image = null;
            this.form.technical_file = null;

            // Si tienes referencias para los inputs de archivo, limpiarlas
            if (this.$refs.invoiceFile) this.$refs.invoiceFile.value = null;
            if (this.$refs.truckConditionImage) this.$refs.truckConditionImage.value = null;
            if (this.$refs.truckPlateImage) this.$refs.truckPlateImage.value = null;
            if (this.$refs.technicalFile) this.$refs.technicalFile.value = null;
        },
        async submitFiles() {
            try {
                const formData = new FormData();

                // Agregar archivos al FormData
                if (this.form.invoice_file) {
                    formData.append('invoice_file', this.form.invoice_file);
                }
                if (this.form.truck_condition_image) {
                    formData.append('truck_condition_image', this.form.truck_condition_image);
                }
                if (this.form.truck_plate_image) {
                    formData.append('truck_plate_image', this.form.truck_plate_image);
                }
                if (this.form.technical_file) {
                    formData.append('technical_file', this.form.technical_file);
                }

                // Agregar proveedor al FormData
                if (this.form.supplier) {
                    formData.append('supplier', this.form.supplier.trim());
                } else {
                    throw new Error("El campo 'Proveedor' no puede estar vacío.");
                }

                if (this.form.product) {
                    formData.append('product', this.form.product.trim());
                } else {
                    throw new Error("El campo 'Producto' no puede estar vacío.");
                }

                // Realizar solicitud
                const response = await axios.post(
                    `${process.env.VUE_APP_API_URL}/api/submit-materials-files`,
                    formData // FormData se maneja automáticamente
                );

                // Verificar si la respuesta es exitosa
                if (response.status === 200) {
                    alert(response.data?.message || "Archivos subidos exitosamente");
                    this.clearFileInputs(); // Limpiar campos
                } else {
                    throw new Error("Error inesperado al procesar la solicitud.");
                }
            } catch (error) {
                console.error("Error al enviar archivos:", error);
                alert(
                    error.response?.data?.error ||
                    "Hubo un error al enviar los archivos. Por favor, inténtelo de nuevo."
                );
            }
        },
        async submitForm() {
            try {
                // Copiar el formulario actual y convertir los valores de texto a mayúsculas
                const formToSubmit = { ...this.form };

                Object.keys(formToSubmit).forEach((key) => {
                    if (typeof formToSubmit[key] === 'string') {
                        formToSubmit[key] = formToSubmit[key].toUpperCase();
                    }
                });

                // Enviar los datos al backend como JSON
                const response = await axios.post(
                    `${process.env.VUE_APP_API_URL}/api/submit-material-form`,
                    formToSubmit,
                    { headers: { 'Content-Type': 'application/json' } }
                );

                // Mostrar mensaje de éxito solo si la respuesta fue satisfactoria
                if (response.status === 200 && response.data?.message) {
                    alert(response.data.message); // Mensaje definido en el backend
                }

                // Reiniciar el formulario
                this.resetForm();
            } catch (error) {
                // Este bloque solo se ejecutará si ocurre un error real
                console.error("Error al guardar el formulario:", error);

                const errorMessage =
                    error.response?.data?.error ||
                    "Hubo un error al guardar el formulario. Por favor, inténtelo de nuevo.";
                alert(errorMessage);
            }
        },
        resetForm() {
            this.form.foreign_bodies = '';
            this.form.lot_number = '';
            this.form.package_quantity = '';
            this.form.total_weight = '';
            this.form.manufacture_date = '';
            this.form.expiry_date = '';
            this.form.shelf_life_check = '';
            this.form.allergen_statement = '';
            this.form.graphic_system = '';
            this.form.product_accepted = '';
            this.form.rejection_reasons = '';

        },
        convertToUppercase(field) {
            this.form[field] = this.form[field]?.toUpperCase() || '';
        },
        async fetchSuppliers() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/providers-material`);
                this.suppliers = response.data; // Suponiendo que el backend devuelve un arreglo de strings
            } catch (error) {
                console.error('Error al obtener proveedores:', error);
            }
        },
        async fetchProducts() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/material`);
                this.products = response.data; // Suponiendo que el backend devuelve un arreglo de strings
            } catch (error) {
                console.error('Error al obtener productos:', error);
            }
        },
        async fetchBrands() {
            try {
                const response = await axios.get(`${process.env.VUE_APP_API_URL}/api/brand`);
                this.brands = response.data; // Suponiendo que el backend devuelve un arreglo de strings
            } catch (error) {
                console.error('Error al obtener marcas:', error);
            }
        }
    },
};
</script>

<style scoped>
input[type="text"] {
    text-transform: uppercase;
}

textarea {
    text-transform: uppercase;
}

.custom-back-button {
    display: flex;
    /* Activa flexbox para alinear elementos */
    align-items: center;
    /* Alinea verticalmente ícono y texto */
    justify-content: center;
    /* Centra contenido horizontalmente dentro del botón */
    background-color: #ffffff;
    /* Cambia al color deseado */
    color: rgb(0, 0, 0);
    /* Texto negro */
    border: none;
    /* Elimina bordes */
    border-radius: 8px;
    /* Bordes redondeados */
    padding: 10px 20px;
    /* Añade espaciado interno */
    font-size: 16px;
    /* Tamaño del texto */
    font-weight: bold;
    /* Hace el texto más visible */
    cursor: pointer;
    /* Cambia el cursor al pasar sobre el botón */
    gap: 10px;
    /* Espaciado entre el ícono y el texto */
    transition: background-color 0.3s;
    /* Animación al cambiar color */
}

/* Cambia el color al pasar el mouse */
.custom-back-button:hover {
    background-color: #e3e6e9;
    /* Cambia ligeramente el color */
}

/* Estilo para el ícono */
.button-icon {
    width: 22px;
    /* Tamaño del ícono */
    height: 22px;
    /* Tamaño del ícono */
}

/* Header que se ajusta automáticamente */
.custom-header {
    display: flex;
    /* Usa flexbox para alinear los elementos */
    align-items: center;
    /* Alinea verticalmente los elementos */
    justify-content: space-between;
    /* Separa el título del botón */
    flex-wrap: wrap;
    /* Permite que el contenido haga wrap si no cabe */
    padding: 10px;
    /* Añade espacio dentro del header */
    gap: 10px;
    /* Espaciado entre los elementos */
}
</style>