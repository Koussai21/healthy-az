<script setup>
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import client from "../api/client";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const posts = ref([]);
const loading = ref(true);
const title = ref("");
const content = ref("");
const err = ref("");

async function load() {
  loading.value = true;
  try {
    const { data } = await client.get("/api/forum/posts");
    posts.value = data;
  } finally {
    loading.value = false;
  }
}

onMounted(load);

async function createPost() {
  err.value = "";
  try {
    await client.post("/api/forum/posts", {
      title: title.value.trim(),
      content: content.value.trim(),
    });
    title.value = "";
    content.value = "";
    await load();
  } catch (e) {
    err.value = e.response?.data?.detail || "Impossible de créer le sujet.";
  }
}
</script>

<template>
  <div>
    <h1 class="h1">Forum</h1>
    <p class="muted">Échangez sur la santé et l'encyclopédie — restez respectueux et factuels.</p>

    <div v-if="auth.isAuthenticated" class="card composer">
      <h2 class="h2">Nouveau sujet</h2>
      <form class="form" @submit.prevent="createPost">
        <div>
          <label class="label" for="t">Titre</label>
          <input id="t" v-model="title" class="input" required />
        </div>
        <div>
          <label class="label" for="c">Message</label>
          <textarea id="c" v-model="content" class="input area" required rows="5" />
        </div>
        <p v-if="err" class="err">{{ err }}</p>
        <button class="btn" type="submit">Publier</button>
      </form>
    </div>
    <p v-else class="card muted">
      <RouterLink to="/connexion">Connectez-vous</RouterLink>
      pour ouvrir un sujet ou répondre.
    </p>

    <p v-if="loading" class="muted">Chargement…</p>
    <ul v-else class="list">
      <li v-for="p in posts" :key="p.id" class="card item">
        <RouterLink class="title" :to="`/forum/${p.id}`">{{ p.title }}</RouterLink>
        <p class="meta muted">
          Par {{ p.author_username }} · {{ new Date(p.created_at).toLocaleString("fr-FR") }}
        </p>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.composer {
  margin: 1.25rem 0;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  margin-top: 0.5rem;
}

.area {
  resize: vertical;
}

.err {
  color: var(--danger);
  margin: 0;
  font-size: 0.9rem;
}

.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.item .title {
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--text);
  text-decoration: none;
}

.item .title:hover {
  color: var(--accent);
}

.meta {
  margin: 0.35rem 0 0;
  font-size: 0.85rem;
}
</style>
