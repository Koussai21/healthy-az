<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import client from "../api/client";

const router = useRouter();
const form = reactive({
  kind: "symptome",
  title: "",
  summary: "",
  content: "",
});
const err = ref("");
const loading = ref(false);

async function submit() {
  err.value = "";
  loading.value = true;
  try {
    const { data } = await client.post("/api/encyclopedia", { ...form });
    router.push(`/fiche/${data.slug}`);
  } catch (e) {
    err.value = e.response?.data?.detail || "Impossible d'enregistrer la fiche.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="card narrow">
    <h1 class="h1">Nouvelle fiche</h1>
    <p class="muted">Ajoutez une maladie, un symptôme ou un diagnostic à l'encyclopédie.</p>
    <form class="form" @submit.prevent="submit">
      <div>
        <label class="label" for="k">Type</label>
        <select id="k" v-model="form.kind" class="input">
          <option value="maladie">Maladie</option>
          <option value="symptome">Symptôme</option>
          <option value="diagnostic">Diagnostic</option>
        </select>
      </div>
      <div>
        <label class="label" for="t">Titre</label>
        <input id="t" v-model="form.title" class="input" required maxlength="300" />
      </div>
      <div>
        <label class="label" for="s">Résumé court (optionnel)</label>
        <input id="s" v-model="form.summary" class="input" />
      </div>
      <div>
        <label class="label" for="c">Contenu</label>
        <textarea id="c" v-model="form.content" class="input area" required rows="10" />
      </div>
      <p v-if="err" class="err">{{ err }}</p>
      <button class="btn" type="submit" :disabled="loading">{{ loading ? "Publication…" : "Publier" }}</button>
    </form>
  </div>
</template>

<style scoped>
.narrow {
  max-width: 720px;
  margin: 0 auto;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.25rem;
}

.area {
  resize: vertical;
  min-height: 200px;
}

.err {
  color: var(--danger);
  margin: 0;
}
</style>
