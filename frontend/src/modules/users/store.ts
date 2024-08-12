import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useUsersStore = defineStore("users", () => {
  const userMe = ref<{
    id: number;
    email: string;
    full_name: string;
    is_active: boolean;
    is_admin: boolean;
    is_master: boolean;
    companies: object[];
  }>();

  const canUsers = computed(() => {
    return userMe.value?.is_admin;
  });

  const canCreate = computed(() => {
    return userMe.value?.is_admin;
  });

  const canDelete = computed(() => {
    return userMe.value?.is_admin;
  });

  function logout() {
    userMe.value = undefined;
  }

  return {
    userMe,
    canUsers,
    canCreate,
    canDelete,
    logout,
  };
});
