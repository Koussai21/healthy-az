<script setup>
import { onMounted, ref, watch } from "vue";
import client from "../api/client";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const conversations = ref([]);
const users = ref([]);
const peerId = ref(null);
const thread = ref([]);
const draft = ref("");
const userQuery = ref("");
const err = ref("");

async function loadConversations() {
  const { data } = await client.get("/api/messages/conversations");
  conversations.value = data;
}

async function loadUsers() {
  const { data } = await client.get("/api/messages/users", {
    params: userQuery.value.trim() ? { q: userQuery.value.trim() } : {},
  });
  users.value = data;
}

async function loadThread(id) {
  const { data } = await client.get(`/api/messages/with/${id}`);
  thread.value = data;
}

async function send() {
  err.value = "";
  if (!peerId.value || !draft.value.trim()) return;
  try {
    await client.post("/api/messages", { recipient_id: peerId.value, content: draft.value.trim() });
    draft.value = "";
    await loadThread(peerId.value);
    await loadConversations();
  } catch (e) {
    err.value = e.response?.data?.detail || "Envoi impossible.";
  }
}

onMounted(async () => {
  await loadConversations();
  await loadUsers();
});

let userTimer;
watch(userQuery, () => {
  clearTimeout(userTimer);
  userTimer = setTimeout(loadUsers, 250);
});

watch(peerId, (id) => {
  if (id) loadThread(id);
  else thread.value = [];
});
</script>

<template>
  <div class="grid-layout">
    <aside class="card aside">
      <h2 class="h2">Conversations</h2>
      <ul class="conv-list">
        <li v-for="c in conversations" :key="c.user_id">
          <button type="button" class="conv" :class="{ active: peerId === c.user_id }" @click="peerId = c.user_id">
            <span class="uname">{{ c.username }}</span>
            <span v-if="c.unread_count" class="unread">{{ c.unread_count }}</span>
            <span v-if="c.last_preview" class="preview muted">{{ c.last_preview }}</span>
          </button>
        </li>
      </ul>
      <p v-if="conversations.length === 0" class="muted small">Aucune conversation pour l'instant.</p>

      <h2 class="h2 spaced">Écrire à…</h2>
      <input v-model="userQuery" class="input" placeholder="Rechercher un membre" />
      <ul class="user-list">
        <li v-for="u in users" :key="u.id">
          <button type="button" class="user-pick" @click="peerId = u.id">{{ u.username }}</button>
        </li>
      </ul>
    </aside>

    <section class="card chat">
      <template v-if="peerId">
        <h2 class="h2">Discussion</h2>
        <div class="thread">
          <div
            v-for="m in thread"
            :key="m.id"
            class="bubble"
            :class="{ me: m.sender_id === auth.user?.id }"
          >
            <span class="who muted">{{ m.sender_username }}</span>
            <p class="text">{{ m.content }}</p>
            <span class="when muted">{{ new Date(m.created_at).toLocaleString("fr-FR") }}</span>
          </div>
        </div>
        <form class="send" @submit.prevent="send">
          <textarea v-model="draft" class="input area" rows="3" placeholder="Votre message…" />
          <p v-if="err" class="err">{{ err }}</p>
          <button class="btn" type="submit">Envoyer</button>
        </form>
      </template>
      <p v-else class="muted">Choisissez une conversation ou un utilisateur.</p>
    </section>
  </div>
</template>

<style scoped>
.grid-layout {
  display: grid;
  gap: 1rem;
}

@media (min-width: 900px) {
  .grid-layout {
    grid-template-columns: 300px 1fr;
    align-items: start;
  }
}

.aside {
  padding: 1rem;
}

.spaced {
  margin-top: 1.25rem;
}

.conv-list,
.user-list {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0;
}

.conv,
.user-pick {
  width: 100%;
  text-align: left;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: 10px;
  padding: 0.5rem 0.65rem;
  margin-bottom: 0.4rem;
  cursor: pointer;
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  align-items: center;
}

.conv.active {
  border-color: rgba(94, 234, 212, 0.45);
  box-shadow: 0 0 0 2px rgba(94, 234, 212, 0.12);
}

.uname {
  font-weight: 600;
}

.unread {
  font-size: 0.7rem;
  background: var(--danger);
  color: #0a0f18;
  padding: 0.1rem 0.45rem;
  border-radius: 999px;
  font-weight: 700;
}

.preview {
  width: 100%;
  font-size: 0.8rem;
  display: block;
}

.small {
  font-size: 0.85rem;
}

.chat {
  min-height: 420px;
  display: flex;
  flex-direction: column;
}

.thread {
  flex: 1;
  overflow-y: auto;
  max-height: 480px;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  margin: 0.5rem 0 1rem;
  padding-right: 0.25rem;
}

.bubble {
  align-self: flex-start;
  max-width: 85%;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 0.65rem 0.85rem;
}

.bubble.me {
  align-self: flex-end;
  border-color: rgba(94, 234, 212, 0.25);
}

.who {
  font-size: 0.75rem;
}

.text {
  margin: 0.25rem 0;
  white-space: pre-wrap;
  line-height: 1.45;
}

.when {
  font-size: 0.72rem;
}

.send {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.area {
  resize: vertical;
}

.err {
  color: var(--danger);
  margin: 0;
}
</style>
