import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("../views/HomeView.vue"),
  },
  {
    path: "/inscription",
    name: "register",
    component: () => import("../views/RegisterView.vue"),
  },
  {
    path: "/connexion",
    name: "login",
    component: () => import("../views/LoginView.vue"),
  },
  {
    path: "/encyclopedie",
    name: "encyclopedia",
    component: () => import("../views/EncyclopediaView.vue"),
  },
  {
    path: "/encyclopedie/nouveau",
    name: "encyclopedia-new",
    component: () => import("../views/EncyclopediaNewView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/fiche/:slug",
    name: "encyclopedia-detail",
    component: () => import("../views/EncyclopediaDetailView.vue"),
  },
  {
    path: "/forum",
    name: "forum",
    component: () => import("../views/ForumView.vue"),
  },
  {
    path: "/forum/:id",
    name: "forum-detail",
    component: () => import("../views/ForumDetailView.vue"),
  },
  {
    path: "/messages",
    name: "messages",
    component: () => import("../views/MessagesView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/assistant",
    name: "assistant",
    component: () => import("../views/AssistantView.vue"),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: "login", query: { redirect: to.fullPath } };
  }
  return true;
});

export default router;
