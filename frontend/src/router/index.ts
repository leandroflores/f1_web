import { createRouter, createWebHistory } from "vue-router";
import baseRoutes from "./routes";
import { useUsersStore } from "@/modules/users/store";
import axios from "axios";

const router = createRouter({
  history: createWebHistory("/app"),
  routes: [...baseRoutes],
});

router.beforeEach(async (to, from, next) => {
  const store = useUsersStore();
  const DEFAULT_TITLE = "Formula 1";
  document.title = (to.meta.title as string) || DEFAULT_TITLE;

  if (!store.userMe) {
    try {
      const res = await axios.get("/users/me");
      store.userMe = res.data;
    } catch (err) {
      store.$reset();
    }
  }

  if (!store.userMe && to.name !== "login") {
    next({ name: "login", query: { nextUrl: to.fullPath } });
  } else {
    next();
  }
});

export default router;
