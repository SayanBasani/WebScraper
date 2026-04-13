import axios from "axios";
import ENV from "./config/env";
// export const backend_Url = "http://localhost:8000";  // FastAPI port
export const backend_Url = ENV.backend_Url;  // FastAPI port
// export const backend_Url = "https://webscraper-backend-h7dc.onrender.com";  // FastAPI deployed url


const api = axios.create({
    baseURL: `${backend_Url}/`, // change to your backend URL
    withCredentials: true, // needed if backend uses cookies for auth
});
api.defaults.withCredentials = true;


export default api;


