<script setup>
import { onMounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";
import client from "../api/client";
import { useAuthStore } from "../stores/auth";

const route = useRoute();
const auth = useAuthStore();
const post = ref(null);
const err = ref("");
const reply = ref("");
const replyErr = ref("");

async function load() {
  try {
    const { data } = await client.get(`/api/forum/posts/${route.params.id}`);
    post.value = data;
  } catch {
    err.value = "Sujet introuvable.";
  }
}

onMounted(load);

async function sendReply() {
  replyErr.value = "";
  try {
    await client.post(`/api/forum/posts/${route.params.id}/replies`, { content: reply.value.trim() });
    reply.value = "";
    await load();
  } catch (e) {
    replyErr.value = e.response?.data?.detail || "Réponse refusée.";
  }
}
</script>

<template>
  <div v-if="err" class="card">
    <p class="muted">{{ err }}</p>
  </div>
  <div v-else-if="post">
    <p class="muted">
      <RouterLink to="/forum">← Retour au forum</RouterLink>
    </p>
    <article class="card">
      <h1 class="h1">{{ post.title }}</h1>
      <p class="meta muted">
        Par {{ post.author_username }} · {{ new Date(post.created_at).toLocaleString("fr-FR") }}
      </p>
      <div class="body">{{ post.content }}</div>
    </article>

    <section class="replies">
      <h2 class="h2">Réponses ({{ post.replies.length }})</h2>
      <div v-for="r in post.replies" :key="r.id" class="card reply">
        <p class="meta muted">
          {{ r.author_username }} · {{ new Date(r.created_at).toLocaleString("fr-FR") }}
        </p>
        <div class="body">{{ r.content }}</div>
      </div>
    </section>

    <div v-if="auth.isAuthenticated" class="card">
      <h2 class="h2">Votre réponse</h2>
      <form class="form" @submit.prevent="sendReply">
        <textarea v-model="reply" class="input area" required rows="4" />
        <p v-if="replyErr" class="err">{{ replyErr }}</p>
        <button class="btn" type="submit">Envoyer</button>
      </form>
    </div>
    <p v-else class="muted">
      <RouterLink to="/connexion">Connectez-vous</RouterLink>
      pour répondre.
    </p>
  </div>
  <p v-else class="muted">Chargement…</p>
</template>

<style scoped>
.meta {
  font-size: 0.9rem;
}

.body {
  margin-top: 0.75rem;
  white-space: pre-wrap;
  line-height: 1.6;
}

.replies {
  margin-top: 1.25rem;
}

.reply {
  margin-bottom: 0.75rem;
}

.reply .body {
  margin-top: 0.35rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.area {
  resize: vertical;
}

.err {
  color: var(--danger);
  margin: 0;
}
</style>
