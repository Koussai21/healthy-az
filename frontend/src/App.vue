<script setup>
import { onMounted } from "vue";
import AppLayout from "./components/AppLayout.vue";
import { useAuthStore } from "./stores/auth";

const auth = useAuthStore();
onMounted(() => {
  auth.fetchMe();
});
</script>

<template>
  <AppLayout>
    <RouterView v-slot="{ Component }">
      <Transition name="fade" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </AppLayout>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
