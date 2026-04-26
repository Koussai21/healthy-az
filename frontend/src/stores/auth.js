import { defineStore } from "pinia";
import { ref, computed } from "vue";
import client, { setAuthToken } from "../api/client";

const TOKEN_KEY = "healthy_az_token";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || "");
  const user = ref(null);
  const loading = ref(false);
  const error = ref("");

  if (token.value) setAuthToken(token.value);

  const isAuthenticated = computed(() => !!token.value);

  async function fetchMe() {
    if (!token.value) return;
    loading.value = true;
    error.value = "";
    try {
      const { data } = await client.get("/api/users/me");
      user.value = data;
    } catch (e) {
      user.value = null;
      token.value = "";
      localStorage.removeItem(TOKEN_KEY);
      setAuthToken(null);
    } finally {
      loading.value = false;
    }
  }

  function persistToken(t) {
    token.value = t;
    if (t) {
      localStorage.setItem(TOKEN_KEY, t);
      setAuthToken(t);
    } else {
      localStorage.removeItem(TOKEN_KEY);
      setAuthToken(null);
    }
  }

  async function register(payload) {
    loading.value = true;
    error.value = "";
    try {
      const { data } = await client.post("/api/auth/register", payload);
      persistToken(data.access_token);
      await fetchMe();
      return true;
    } catch (e) {
      error.value = e.response?.data?.detail || "Inscription impossible";
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function login(payload) {
    loading.value = true;
    error.value = "";
    try {
      const { data } = await client.post("/api/auth/login", payload);
      persistToken(data.access_token);
      await fetchMe();
      return true;
    } catch (e) {
      error.value = e.response?.data?.detail || "Connexion refusée";
      return false;
    } finally {
      loading.value = false;
    }
  }

  function logout() {
    user.value = null;
    persistToken("");
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    fetchMe,
    register,
    login,
    logout,
  };
});
