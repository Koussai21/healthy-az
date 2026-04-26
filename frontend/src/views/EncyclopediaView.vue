<script setup>
import { onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";
import client from "../api/client";

const q = ref("");
const kind = ref("");
const items = ref([]);
const loading = ref(false);

async function load() {
  loading.value = true;
  try {
    const params = {};
    if (q.value.trim()) params.q = q.value.trim();
    if (kind.value) params.kind = kind.value;
    const { data } = await client.get("/api/encyclopedia", { params });
    items.value = data;
  } finally {
    loading.value = false;
  }
}

onMounted(load);
let debounceTimer;
watch([q, kind], () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(load, 280);
});

function kindLabel(k) {
  if (k === "maladie") return "Maladie";
  if (k === "symptome") return "Symptôme";
  if (k === "diagnostic") return "Diagnostic";
  return k;
}
</script>

<template>
  <div>
    <div class="head card">
      <h1 class="h1">Encyclopédie</h1>
      <p class="muted">
        Recherche libre sur les titres, résumés et contenus — comme une recherche « naturelle » sur le web.
      </p>
      <div class="toolbar">
        <input
          v-model="q"
          class="input search"
          type="search"
          placeholder="Ex. : maux de tête persistants, hypertension, fièvre…"
          aria-label="Recherche"
        />
        <select v-model="kind" class="input select">
          <option value="">Tous les types</option>
          <option value="maladie">Maladies</option>
          <option value="symptome">Symptômes</option>
          <option value="diagnostic">Diagnostics</option>
        </select>
        <RouterLink class="btn" to="/encyclopedie/nouveau">Nouvelle fiche</RouterLink>
      </div>
    </div>

    <p v-if="loading" class="muted">Chargement…</p>
    <ul v-else class="list">
      <li v-for="it in items" :key="it.id" class="card item">
        <RouterLink class="title" :to="`/fiche/${it.slug}`">{{ it.title }}</RouterLink>
        <span class="badge">{{ kindLabel(it.kind) }}</span>
        <p v-if="it.summary" class="muted summary">{{ it.summary }}</p>
      </li>
    </ul>
    <p v-if="!loading && items.length === 0" class="muted">Aucun résultat. Essayez d'autres mots ou ajoutez une fiche.</p>
  </div>
</template>

<style scoped>
.head {
  margin-bottom: 1.25rem;
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1rem;
  align-items: center;
}

.search {
  flex: 1 1 220px;
}

.select {
  flex: 0 1 180px;
}

.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.item {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.35rem 1rem;
  align-items: start;
}

.title {
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--text);
  text-decoration: none;
}

.title:hover {
  color: var(--accent);
}

.summary {
  grid-column: 1 / -1;
  margin: 0;
  font-size: 0.95rem;
}

.badge {
  font-family: var(--mono);
  font-size: 0.7rem;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
</style>
