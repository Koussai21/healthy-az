<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import client from "../api/client";

const route = useRoute();
const item = ref(null);
const err = ref("");

function kindLabel(k) {
  if (k === "maladie") return "Maladie";
  if (k === "symptome") return "Symptôme";
  if (k === "diagnostic") return "Diagnostic";
  return k;
}

onMounted(async () => {
  try {
    const { data } = await client.get(`/api/encyclopedia/${route.params.slug}`);
    item.value = data;
  } catch {
    err.value = "Fiche introuvable.";
  }
});
</script>

<template>
  <div v-if="err" class="card">
    <p class="muted">{{ err }}</p>
  </div>
  <article v-else-if="item" class="card article">
    <p class="badge">{{ kindLabel(item.kind) }}</p>
    <h1 class="h1">{{ item.title }}</h1>
    <p v-if="item.summary" class="lead muted">{{ item.summary }}</p>
    <div class="body">{{ item.content }}</div>
  </article>
  <p v-else class="muted">Chargement…</p>
</template>

<style scoped>
.article {
  max-width: 820px;
}

.badge {
  display: inline-block;
  font-family: var(--mono);
  font-size: 0.72rem;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 0.5rem;
}

.lead {
  font-size: 1.05rem;
  line-height: 1.5;
}

.body {
  margin-top: 1.25rem;
  white-space: pre-wrap;
  line-height: 1.65;
  color: var(--text);
}
</style>
