import axios from "axios";
import { ref } from "vue";
import { useSnackbar } from "@/store";

export const useLoadCompanies = () => {
  const { showSnackbar } = useSnackbar();
  const unexpectedError =
    "Erro inesperado. Tente novamente ou entre em contato com o suporte.";
  const loadingCompanies = ref(false);
  const companies = ref<any[]>([]);

  async function load() {
    try {
      loadingCompanies.value = true;
      const res = await axios.get("/companies");
      companies.value = res.data;
    } catch (err) {
      showSnackbar(unexpectedError, "error");
    } finally {
      loadingCompanies.value = false;
    }
  }

  return {
    loadingCompanies: loadingCompanies,
    companies: companies,
    load,
  };
};

export const useLoadOrganizations = () => {
  const { showSnackbar } = useSnackbar();
  const unexpectedError =
    "Erro inesperado. Tente novamente ou entre em contato com o suporte.";
  const loadingOrganizations = ref(false);
  const organizations = ref<any[]>([]);

  async function load() {
    try {
      loadingOrganizations.value = true;
      const res = await axios.get("/organizations");
      organizations.value = res.data;
    } catch (err) {
      showSnackbar(unexpectedError, "error");
    } finally {
      loadingOrganizations.value = false;
    }
  }

  return {
    loadingOrganizations,
    organizations,
    load,
  };
};
