import axios from 'axios';


const apiUrl = process.env.VUE_APP_API_URL;

export const api = axios.create({
  baseURL: apiUrl
});

export default api;