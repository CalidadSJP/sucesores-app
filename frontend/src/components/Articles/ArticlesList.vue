<template>
    <div class="container">
        <h1 class="page-title">Gestión de Productos</h1>

        <!-- Tarjeta de Agregar/Editar Artículo -->
        <div class="card card-custom w-100 mb-4">
            <div class="card-body">
                <h5 class="card-title">{{ isEditing ? 'Editar' : 'Agregar' }} Producto</h5><br>
                <form @submit.prevent="isEditing ? updateArticle() : addArticle()">
                    <div class="row">
                        <div class="form-group col-md-6">
                            <label for="cod_article">Código</label>
                            <input v-model="article.cod_article" type="text" @input="toUpper('article', 'cod_article')"
                                class="form-control" id="cod_article" />
                        </div>
                        <div class="form-group col-md-6">
                            <label for="article_name">Nombre</label>
                            <input v-model="article.article_name" @input="toUpper('article', 'article_name')"
                                type="text" class="form-control" id="article_name" />
                        </div>
                        <div class="form-group col-md-6">
                            <label for="format">Formato</label>
                            <input v-model="article.format" type="text" @input="toUpper('article', 'format')"
                                class="form-control" id="format" />
                        </div>
                        <div class="form-group col-md-6">
                            <label for="brand_id">Marca</label>
                            <select v-model="article.brand_id" class="form-control" id="brand_id">
                                <option v-for="brand in brands" :key="brand.id" :value="brand.id">{{ brand.name }}
                                </option>
                            </select>
                        </div>
                        <div class="form-group col-md-6">
                            <label for="ean13">EAN13</label>
                            <input v-model="article.ean13" type="text" class="form-control" id="ean13" />
                        </div>
                        <div class="form-group col-md-6">
                            <label for="ean14">EAN14</label>
                            <input v-model="article.ean14" type="text" class="form-control" id="ean14" />
                        </div>
                        <div class="form-group col-md-6">
                            <label for="weight">Peso</label>
                            <input v-model="article.weight" type="text" class="form-control" id="weight" />
                        </div>
                    </div><br>
                    <button type="submit" class="btn btn-success me-2">{{ isEditing ? 'Actualizar' : 'Agregar'
                        }}</button>
                    <button type="button" class="btn btn-secondary" @click="cancelEdit">Cancelar</button>
                </form>
            </div>
        </div>

        <!-- Tarjeta de Lista de Artículos -->
        <div class="card card-custom w-100 mb-4">

            <div class="card-body">
                <h5 class="card-title">Lista de Prodcutos</h5>
                <input v-model="searchQuery" type="text" class="form-control mb-3"
                    placeholder="Buscar..." />
                <div class="table-responsive">
                    <table class="table table-striped table-bordered">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Código</th>
                                <th>Nombre</th>
                                <th>Formato</th>
                                <th>Marca</th>
                                <th>EAN13</th>
                                <th>EAN14</th>
                                <th>Peso</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in filteredArticles" :key="item.id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ item.cod_article }}</td>
                                <td>{{ item.article_name }}</td>
                                <td>{{ item.format }}</td>
                                <td>{{ getBrandName(item.brand_id) }}</td>
                                <td>{{ item.ean13 }}</td>
                                <td>{{ item.ean14 }}</td>
                                <td>{{ item.weight }}</td>
                                <td>
                                    <div class="btn-group action-icons">
                                        <button class="btn btn-warning icon-btn me-1" @click="editArticle(item)"
                                            title="Editar">
                                            <img src="@/assets/edit.png" alt="Editar" class="icon" />
                                        </button>
                                        <button class="btn btn-danger icon-btn" @click="deleteArticle(item.id)"
                                            title="Eliminar">
                                            <img src="@/assets/delete.png" alt="Eliminar" class="icon" />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>



<script>
import axios from 'axios';

export default {
    data() {
        return {
            article: {
                id: null,
                cod_article: '',
                article_name: '',
                format: '',
                brand_id: '',
                ean13: '',
                ean14: '',
                weight: ''
            },
            articles: [],
            brands: [],
            isEditing: false,
            searchQuery: ''
        };
    },
    computed: {
        filteredArticles() {
            const query = this.searchQuery.toLowerCase();
            return this.articles.filter(item =>
                item.article_name.toLowerCase().includes(query) ||
                this.getBrandName(item.brand_id).toLowerCase().includes(query) ||
                (item.ean13 && item.ean13.toLowerCase().includes(query)) ||
                (item.ean14 && item.ean14.toLowerCase().includes(query))
            );
        }
    }
    ,
    methods: {
        async fetchArticles() {
            const res = await axios.get(`${process.env.VUE_APP_API_URL}/api/articles`);
            this.articles = res.data;
        },
        async fetchBrands() {
            const res = await axios.get(`${process.env.VUE_APP_API_URL}/api/brands`);
            this.brands = res.data;
        },
        getBrandName(brandId) {
            const brand = this.brands.find(b => b.id === brandId);
            return brand ? brand.name : 'Desconocido';
        },
        async addArticle() {
            await axios.post(`${process.env.VUE_APP_API_URL}/api/articles`, this.article);
            this.fetchArticles();
            this.resetForm();
        },
        async updateArticle() {
            await axios.put(`${process.env.VUE_APP_API_URL}/api/articles/${this.article.id}`, this.article);
            this.fetchArticles();
            this.resetForm();
        },
        async deleteArticle(id) {
            if (confirm("¿Seguro que quieres eliminar este artículo?")) {
                await axios.delete(`${process.env.VUE_APP_API_URL}/api/articles/${id}`);
                this.fetchArticles();
            }
        },
        editArticle(item) {
            this.article = { ...item };
            this.isEditing = true;
            window.scrollTo({ top: 0, behavior: 'smooth' }); // Desplazamiento al tope
        },
        cancelEdit() {
            this.resetForm();
        },
        resetForm() {
            this.article = {
                id: null,
                cod_article: '',
                article_name: '',
                format: '',
                brand_id: '',
                ean13: '',
                ean14: '',
                weight: ''
            };
            this.isEditing = false;
        },
        toUpper(model, field) {
            this[model][field] = this[model][field].toUpperCase();
        }
    },
    mounted() {
        this.fetchArticles();
        this.fetchBrands();
    }
};
</script>

<style scoped>
.container {
    max-width: 1300px;
    margin: 0 auto;
    padding: 20px;
}

.page-title {
    text-align: center;
    margin-bottom: 30px;
}

.card-custom {
    width: 100%;
    max-width: 100%;
    flex: 1 1 auto;
}

.card-body {
    padding: 20px;
}

.table-responsive {
    max-height: 500px;
    overflow-x: auto;
}

.action-button {
    width: 100%;
    /* o el tamaño que desees */
}

input[type="text"],
select,
textarea {
    text-transform: uppercase;
}


/* Contenedor para alinear correctamente */
.action-buttons {
    display: inline-flex;
    white-space: nowrap;
}

.icon-btn {
    width: 36px;
    height: 36px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0;
    /* recto por defecto */
}

/* Ícono dentro del botón */
.icon {
    width: 20px;
    height: 20px;
    display: block;
    margin: 0 auto;
}

/* Alineación horizontal */
.action-icons {
    display: inline-flex;
}

/* Bordes redondeados externos */
.action-icons .btn:first-child {
    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
}

.action-icons .btn:last-child {
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}

.form-control {
    font-weight: 400 !important;
}
</style>