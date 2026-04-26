<script setup>
import { ref } from "vue";
import client from "../api/client";

const input = ref("");
const messages = ref([
  {
    role: "assistant",
    text: "Bonjour. Je suis l'assistant Healthy-AZ (Phi‑3 via Ollama). Posez une question générale sur la santé — je rappellerai qu'un médecin reste indispensable pour un diagnostic.",
  },
]);
const loading = ref(false);
const err = ref("");

async function send() {
  const q = input.value.trim();
  if (!q || loading.value) return;
  err.value = "";
  messages.value.push({ role: "user", text: q });
  input.value = "";
  loading.value = true;
  try {
    const { data } = await client.post("/api/chat/assistant", { message: q });
    messages.value.push({ role: "assistant", text: data.reply });
  } catch (e) {
    err.value =
      e.response?.data?.detail ||
      "Impossible de joindre Ollama. Vérifiez qu'il tourne et que le modèle phi3 est tiré (`ollama pull phi3`).";
    messages.value.push({
      role: "assistant",
      text: "Désolé, une erreur s'est produite. Vérifiez la configuration Ollama côté serveur.",
    });
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="card wrap">
    <h1 class="h1">Assistant IA</h1>
    <p class="muted">
      Modèle local via Ollama (par défaut <code>phi3</code>). Les réponses sont informatives uniquement.
    </p>
    <p v-if="err" class="err">{{ err }}</p>
    <div class="chat">
      <div
        v-for="(m, i) in messages"
        :key="i"
        class="msg"
        :class="m.role"
      >
        {{ m.text }}
      </div>
      <p v-if="loading" class="muted">Réflexion en cours…</p>
    </div>
    <form class="form" @submit.prevent="send">
      <textarea v-model="input" class="input area" rows="3" placeholder="Votre question…" />
      <button class="btn" type="submit" :disabled="loading">Envoyer</button>
    </form>
  </div>
</template>

<style scoped>
.wrap {
  max-width: 720px;
  margin: 0 auto;
}

code {
  font-family: var(--mono);
  font-size: 0.85em;
  color: var(--accent);
}

.err {
  color: var(--danger);
  font-size: 0.9rem;
}

.chat {
  margin: 1rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  max-height: 420px;
  overflow-y: auto;
  padding-right: 0.25rem;
}

.msg {
  padding: 0.75rem 1rem;
  border-radius: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
  border: 1px solid var(--border);
}

.msg.user {
  align-self: flex-end;
  background: rgba(94, 234, 212, 0.1);
}

.msg.assistant {
  align-self: flex-start;
  background: var(--bg-elevated);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.area {
  resize: vertical;
}
</style>
