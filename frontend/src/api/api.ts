import axios from "axios";

const API_BASE = "http://localhost:8000"; // adjust if using Docker
const API_KEY = "mysecretkey"; // must match backend

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "X-API-KEY": API_KEY,
  },
});

export default api;
