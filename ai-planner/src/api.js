import axios from "axios";
import { supabase } from "./supabaseClient";

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  }
});

// Request interceptor to attach token
api.interceptors.request.use(
  async (config) => {
    // 1. Get the session properly (supabase.auth.getSession() returns a Promise)
    const { data } = await supabase.auth.getSession();
    const token = data.session?.access_token;

    // 2. If token exists, attach it to the Authorization header
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;