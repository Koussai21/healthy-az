<script setup>
import { reactive } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();
const form = reactive({ username: "", password: "" });

async function submit() {
  const ok = await auth.login({ ...form });
  if (ok) {
    const redir = route.query.redirect;
    router.push(typeof redir === "string" ? redir : "/encyclopedie");
  }
}
</script>

<template>
  <div class="narrow card">
    <h1 class="h1">Connexion</h1>
    <p class="muted">Accédez au forum, à la messagerie et à l'assistant IA.</p>
    <form class="form" @submit.prevent="submit">
      <div>
        <label class="label" for="un">Nom d'utilisateur</label>
        <input id="un" v-model="form.username" class="input" required autocomplete="username" />
      </div>
      <div>
        <label class="label" for="pw">Mot de passe</label>
        <input
          id="pw"
          v-model="form.password"
          class="input"
          type="password"
          required
          autocomplete="current-password"
        />
      </div>
      <p v-if="auth.error" class="err">{{ auth.error }}</p>
      <button class="btn" type="submit" :disabled="auth.loading">
        {{ auth.loading ? "Connexion…" : "Se connecter" }}
      </button>
    </form>
    <p class="muted foot">
      Pas encore de compte ?
      <RouterLink to="/inscription">S'inscrire</RouterLink>
    </p>
  </div>
</template>

<style scoped>
.narrow {
  max-width: 420px;
  margin: 0 auto;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.25rem;
}

.err {
  color: var(--danger);
  margin: 0;
  font-size: 0.9rem;
}

.foot {
  margin-top: 1.25rem;
}
</style>
