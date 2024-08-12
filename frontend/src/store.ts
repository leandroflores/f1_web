import { defineStore } from "pinia";
import { ref } from "vue";

export const useSnackbar = defineStore("snackbar", () => {
  const snackbar = ref(false);
  const snackbarMsg = ref("");
  const snackbarColor = ref("");

  function showSnackbar(msg: string, color: string) {
    snackbar.value = true;
    snackbarMsg.value = msg;
    snackbarColor.value = color;
  }

  function resetSnackbar() {
    snackbar.value = false;
    snackbarMsg.value = "";
    snackbarColor.value = "";
  }

  function $reset() {
    resetSnackbar();
  }

  return { snackbar, snackbarMsg, snackbarColor, showSnackbar, resetSnackbar };
});
