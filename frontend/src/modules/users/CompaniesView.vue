<template>
  <v-container fluid class="bg-white">
    <CRUDTable
      v-model:create-form-data="createFormData"
      v-model:edit-form-data="editFormData"
      :url-base="urlBase"
      :messages="crudMsgs"
      :create-config="createConfig"
      :edit-config="editConfig"
      :headers="tableHeaders"
      :items-process="companiesProcess"
      @create-opened="loadAll"
      @edit-opened="loadAll"
    >
      <template v-slot:[`item.is_active`]="{ item }">
        <v-icon
          :icon="item.is_active ? 'mdi-check' : 'mdi-cancel'"
          :color="item.is_active ? 'success' : 'error'"
        ></v-icon>
      </template>

      <template v-slot:createForm>
        <v-text-field
          label="Nome"
          name="name"
          :error-messages="nameError"
          v-model="createFormData.name"
          validate-on="blur"
          :rules="[required]"
          autofocus
          ref="nameInput"
        ></v-text-field>
        <v-autocomplete
          clearable
          label="Organização"
          auto-select-first
          name="organization"
          v-model="createFormData.organization_id"
          autocomplete="off"
          :items="organizations"
          :loading="loadingOrganizations"
          item-title="name"
          item-value="id"
          validate-on="blur"
          :rules="[required]"
        ></v-autocomplete>
        <v-checkbox
          label="Ativo"
          name="is_active"
          v-model="createFormData.is_active"
          hide-details
          single-line
        ></v-checkbox>
      </template>

      <template v-slot:editForm>
        <v-text-field
          label="Nome"
          name="name"
          :error-messages="nameError"
          v-model="editFormData.name"
          validate-on="blur"
          :rules="[required]"
          autofocus
          ref="nameInput"
        ></v-text-field>
        <v-autocomplete
          clearable
          label="Organização"
          auto-select-first
          name="organization"
          v-model="editFormData.organization_id"
          autocomplete="off"
          :items="organizations"
          :loading="loadingOrganizations"
          item-title="name"
          item-value="id"
          validate-on="blur"
          :rules="[required]"
        ></v-autocomplete>
        <v-checkbox
          label="Ativo"
          name="is_active"
          v-model="editFormData.is_active"
          hide-details
          single-line
        ></v-checkbox>
      </template>
    </CRUDTable>
  </v-container>
</template>

<script setup lang="ts">
import CRUDTable from "@/components/CRUDTable.vue";
import { useLoadOrganizations } from "@/composables/load-organizations";
import { localeDateTimeOptions } from "@/consts";
import { required } from "@/validators";
import { watchOnce } from "@vueuse/core";
import { AxiosError } from "axios";
import { reactive, ref } from "vue";

const defaultCreateFormData = {
  name: "",
  organization_id: undefined,
  is_active: true,
};
const defaultEditFormData = {
  name: "",
  organization_id: undefined,
  is_active: true,
};
const createFormData = reactive({ ...defaultCreateFormData });
const editFormData = reactive({ ...defaultEditFormData });
const urlBase = "/companies";
const crudMsgs = {
  unexpectedError:
    "Erro inesperado. Tente novamente ou entre em contato com o suporte.",
  createSuccess: "Empresa criada com sucesso!",
  editSuccess: "Empresa editada com sucesso!",
};
const createConfig = {
  btnText: "Nova Empresa",
  btnIcon: "mdi-plus",
  formTitle: "Nova Empresa",
  formIcon: "mdi-briefcase-plus",
  submitText: "Salvar",
  formDataDefault: defaultCreateFormData,
  handleCreateError: checkExistingName,
};
const editConfig = {
  btnText: "Editar Empresa",
  formTitle: "Editando Empresa",
  formIcon: "mdi-briefcase-edit",
  submitText: "Salvar",
  formDataDefault: defaultEditFormData,
  handleEditError: checkExistingName,
};

const tableHeaders = [
  {
    title: "ID",
    key: "id",
  },
  {
    title: "Nome",
    key: "name",
  },
  {
    title: "Criação",
    key: "created_at",
  },
  {
    title: "Ativa",
    key: "is_active",
  },
  {
    title: "Organização",
    key: "organization.name",
  },
  {
    title: "Ações",
    key: "actions",
    sortable: false,
    align: "end",
  },
];

const nameError = ref("");
const nameInput = ref();
const existingNameMsg = "Empresa com este nome já existe";

function checkExistingName(err: AxiosError<any, any>) {
  if (err.response?.status === 409) {
    nameError.value = existingNameMsg;
    nameInput.value.focus();
    watchOnce(
      () => createFormData.name || editFormData.name,
      () => (nameError.value = "")
    );
    return true;
  }
  return false;
}

const {
  organizations,
  loadingOrganizations,
  load: loadOrgs,
} = useLoadOrganizations();

function companiesProcess(companies: any[]) {
  return companies.map((company) => {
    company.created_at = new Date(company.created_at).toLocaleString(
      undefined,
      localeDateTimeOptions
    );
    company.organization_id = company.organization?.id;
    return company;
  });
}
async function loadAll() {
  await Promise.all([loadOrgs()]);
}
</script>
