import axios from "axios";
import { ref } from "vue";
import { useSnackbar } from "@/store";

export const useLoadSearches = () => {
  const { showSnackbar } = useSnackbar();
  const unexpectedError =
    "Erro inesperado. Tente novamente ou entre em contato com o suporte.";
  const loadingSearches = ref(false);
  const searches = ref<any[]>([]);

  async function load() {
    try {
      loadingSearches.value = true;
      const res = await axios.get("/searches");
      searches.value = res.data;
    } catch (err) {
      showSnackbar(unexpectedError, "error");
    } finally {
      loadingSearches.value = false;
    }
  }

  return {
    loadingSearches: loadingSearches,
    searches: searches,
    load,
  };
};
