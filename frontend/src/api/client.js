// src/api/client.js
import axios from "axios";
// import { toast } from "react-toastify";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  //   withCredentials: true,
});

// // Optional: handle errors
// api.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     if (error.response?.status === 401) {
//       window.location.href = "/sign-in"; // Redirect to login
//     } else {
//       toast.error("A network error occurred. Please try again.");
//     }
//     return Promise.reject(error);
//   }
// );

export default api;
