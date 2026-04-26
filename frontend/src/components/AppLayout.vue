<script setup>
import { RouterLink, useRoute } from "vue-router";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const route = useRoute();

function isActive(prefix) {
  return route.path === prefix || route.path.startsWith(prefix + "/");
}
</script>

<template>
  <div class="layout">
    <header class="header card">
      <RouterLink to="/" class="brand">
        <span class="brand-mark" aria-hidden="true" />
        <span class="brand-text">Healthy-AZ</span>
      </RouterLink>
      <nav class="nav">
        <RouterLink :class="{ active: isActive('/encyclopedie') }" to="/encyclopedie">Encyclopédie</RouterLink>
        <RouterLink :class="{ active: isActive('/forum') }" to="/forum">Forum</RouterLink>
        <RouterLink v-if="auth.isAuthenticated" :class="{ active: isActive('/messages') }" to="/messages">
          Messages
        </RouterLink>
        <RouterLink v-if="auth.isAuthenticated" :class="{ active: isActive('/assistant') }" to="/assistant">
          Assistant IA
        </RouterLink>
        <template v-if="!auth.isAuthenticated">
          <RouterLink to="/connexion">Connexion</RouterLink>
          <RouterLink class="pill" to="/inscription">Inscription</RouterLink>
        </template>
        <template v-else>
          <span class="user muted">{{ auth.user?.username }}</span>
          <button type="button" class="btn btn-ghost btn-small" @click="auth.logout()">Déconnexion</button>
        </template>
      </nav>
    </header>
    <main class="main">
      <slot />
    </main>
    <footer class="footer muted">
      <p>
        Healthy-AZ est un projet éducatif — les informations ne remplacent pas un avis médical.
      </p>
    </footer>
  </div>
</template>

<style scoped>
.layout {
  max-width: 1120px;
  margin: 0 auto;
  padding: 1.25rem 1.25rem 3rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem 1.25rem;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  color: var(--text);
  text-decoration: none;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.brand:hover {
  text-decoration: none;
}

.brand-mark {
  width: 12px;
  height: 12px;
  background: var(--accent);
  box-shadow: 0 0 12px var(--pixel-glow);
  image-rendering: pixelated;
}

.brand-text {
  font-family: var(--mono);
  font-size: 1.05rem;
}

.nav {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem 1rem;
}

.nav a {
  color: var(--text-muted);
  font-weight: 500;
  text-decoration: none;
}

.nav a:hover {
  color: var(--text);
}

.nav a.active,
.nav a.router-link-active {
  color: var(--accent);
}

.pill {
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  background: rgba(94, 234, 212, 0.12);
  border: 1px solid var(--border);
  color: var(--accent) !important;
}

.user {
  font-size: 0.9rem;
}

.btn-small {
  padding: 0.4rem 0.9rem;
  font-size: 0.85rem;
}

.main {
  flex: 1;
}

.footer {
  text-align: center;
  font-size: 0.85rem;
  padding-top: 1rem;
}

.footer p {
  margin: 0;
}
</style>
