<script setup>
import { reactive } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const router = useRouter();
const form = reactive({
  first_name: "",
  last_name: "",
  email: "",
  username: "",
  password: "",
});

async function submit() {
  const ok = await auth.register({ ...form });
  if (ok) router.push("/encyclopedie");
}
</script>

<template>
  <div class="narrow card">
    <h1 class="h1">Inscription</h1>
    <p class="muted">Créez votre compte pour contribuer, poster sur le forum et envoyer des messages.</p>
    <form class="form" @submit.prevent="submit">
      <div class="grid-2">
        <div>
          <label class="label" for="fn">Prénom</label>
          <input id="fn" v-model="form.first_name" class="input" required autocomplete="given-name" />
        </div>
        <div>
          <label class="label" for="ln">Nom</label>
          <input id="ln" v-model="form.last_name" class="input" required autocomplete="family-name" />
        </div>
      </div>
      <div>
        <label class="label" for="em">Adresse e-mail</label>
        <input id="em" v-model="form.email" class="input" type="email" required autocomplete="email" />
      </div>
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
          minlength="8"
          autocomplete="new-password"
        />
      </div>
      <p v-if="auth.error" class="err">{{ auth.error }}</p>
      <button class="btn" type="submit" :disabled="auth.loading">
        {{ auth.loading ? "Création…" : "S'inscrire" }}
      </button>
    </form>
    <p class="muted foot">
      Déjà inscrit ?
      <RouterLink to="/connexion">Se connecter</RouterLink>
    </p>
  </div>
</template>

<style scoped>
.narrow {
  max-width: 520px;
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
