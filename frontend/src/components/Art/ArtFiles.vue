<template>
    <div class="home-wrapper">
        <header class="menu-header">
            <span class="header-title">Artes</span>
            <button @click="goHome" class="circle-btn">
                <i class="fas fa-home"></i>
            </button>
        </header>

        <section class="menu-section">
            <div class="menu-grid">
                <div v-for="(category, index) in categories" :key="index" class="menu-card">
                    <i :class="getIcon(category.path)" class="icon"></i>
                    <h3>{{ category.name }}</h3>

                    <div class="brand-folders">
                        <div v-for="(brand, i) in category.brands" :key="i" class="brand-folder">
                            <div class="brand-header" @click="toggleBrand(category, i)">
                                <i :class="brand.open ? 'fas fa-folder-open' : 'fas fa-folder'"></i>
                                {{ brand.name }}
                            </div>
                            <transition name="fade">
                                <ul v-show="brand.open" class="file-list">
                                    <li v-for="(file, j) in brand.files" :key="j" class="file-item">
                                        <a :href="`${baseUrl}/api/files/${category.path}/${brand.name}/${file}`"
                                            target="_blank">
                                            <i class="fas fa-file-alt"></i> {{ file }}
                                        </a>
                                    </li>
                                </ul>
                            </transition>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>


<script>
import axios from "axios";

export default {
    name: "ArtFiles",
    data() {
        return {
            categories: [],
            baseUrl: process.env.VUE_APP_API_URL || "http://192.168.0.251:8080"
        };
    },
    methods: {
        async fetchPackagingFiles() {
            try {
                const response = await axios.get(`${this.baseUrl}/api/get-packaging-files`);
                if (response.status === 200) {
                    this.categories = response.data.map((cat) => ({
                        ...cat,
                        brands: cat.brands.map((b) => ({
                            ...b,
                            open: false
                        }))
                    }));
                } else {
                    console.error("Error al obtener archivos de empaque.");
                }
            } catch (error) {
                console.error("Error al obtener archivos de empaque:", error);
                alert("Hubo un error al obtener los archivos de empaque.");
            }
        },
        toggleBrand(category, index) {
            category.brands[index].open = !category.brands[index].open;
        },
        getIcon(categoryPath) {
            const icons = {
                Sacos: "fas fa-rectangle-xmark",
                Rollos: "fas fa-scroll",
                Fundas: "fas fa-shopping-bag",
                Cajas: "fas fa-box"
            };
            return icons[categoryPath] || "fas fa-folder";
        },
        goHome() {
            this.$router.push('/');
        },
    },
    mounted() {
        this.fetchPackagingFiles();
    }
};
</script>

<style scoped>
.home-wrapper {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.menu-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #019c54;
    color: white;
    padding: 20px 40px;
}

.header-title {
    font-size: 1.8rem;
    font-weight: bold;
}

.circle-btn {
    background-color: white;
    color: #019c54;
    border: none;
    border-radius: 50%;
    padding: 12px 16px;
    font-size: 20px;
    cursor: pointer;
    transition: transform 0.2s;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.circle-btn:hover {
    transform: scale(1.1);
}

.menu-section {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 3rem 1rem;
    background: #f0f4f8;
}

.menu-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    padding: 1rem;
}

.menu-card {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    width: 100%;
}

@media (max-width: 768px) {
    .menu-grid {
        grid-template-columns: 1fr;
    }
}

.menu-card:hover {
    transform: translateY(-5px);
}

.icon {
    font-size: 2.5rem;
    color: #019c54;
    margin-bottom: 1rem;
    display: block;
    text-align: center;
}

.brand-folder {
    margin-top: 1rem;
}

.brand-header {
    font-weight: bold;
    cursor: pointer;
    padding: 0.3rem 0.5rem;
    background-color: #f0f0f0;
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.file-list {
    list-style: none;
    padding-left: 1.2rem;
    margin-top: 0.5rem;
}

.file-item {
    margin-bottom: 0.3rem;
}

.file-item a {
    color: #333;
    text-decoration: none;
}

.file-item a:hover {
    text-decoration: underline;
    color: #019c54;
}

.footer {
    text-align: center;
    padding: 1rem;
    background-color: #f0f4f8;
    color: #555;
}
</style>