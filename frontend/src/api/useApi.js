// src/api/useApi.js
import { useEffect } from "react";
import { useAuth } from "@clerk/clerk-react";
import { api } from "./client";

export function useApi() {
  const { getToken, isLoaded } = useAuth();

  useEffect(() => {
    if (!isLoaded) return;
    const id = api.interceptors.request.use(async (config) => {
      const token = await getToken();
      console.log("📥 send token:", token);
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
    return () => api.interceptors.request.eject(id);
  }, [getToken, isLoaded]);

  return api;
}
