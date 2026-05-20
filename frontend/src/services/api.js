import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const API = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

API.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API error:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const predictETA = (payload) =>
  API.post("/predict_eta", payload).then((res) => res.data);

export const getAnalytics = () =>
  API.get("/analytics").then((res) => res.data);

export const getModelMetrics = () =>
  API.get("/model/metrics").then((res) => res.data);

export const submitFeedback = (payload) =>
  API.post("/submit_feedback", payload).then((res) => res.data);

export default API;