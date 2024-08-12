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
      :items-process="organizationsProcess"
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
import { localeDateTimeOptions } from "@/consts";
import { required } from "@/validators";
import { watchOnce } from "@vueuse/core";
import { AxiosError } from "axios";
import { reactive, ref } from "vue";

const defaultCreateFormData = {
  name: "",
  is_active: true,
};
const defaultEditFormData = {
  name: "",
  is_active: true,
};
const createFormData = reactive({ ...defaultCreateFormData });
const editFormData = reactive({ ...defaultEditFormData });
const urlBase = "/organizations";
const crudMsgs = {
  unexpectedError:
    "Erro inesperado. Tente novamente ou entre em contato com o suporte.",
  createSuccess: "Organização criada com sucesso!",
  editSuccess: "Organização editada com sucesso!",
};
const createConfig = {
  btnText: "Nova Organização",
  btnIcon: "mdi-plus",
  formTitle: "Nova Organização",
  formIcon: "mdi-briefcase-plus",
  submitText: "Salvar",
  formDataDefault: defaultCreateFormData,
  handleCreateError: checkExistingName,
};
const editConfig = {
  btnText: "Editar Organização",
  formTitle: "Editando Organização",
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
    title: "Ações",
    key: "actions",
    sortable: false,
    align: "end",
  },
];

const nameError = ref("");
const nameInput = ref();
const existingNameMsg = "Organização com este nome já existe";

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

function organizationsProcess(organizations: any[]) {
  return organizations.map((organization) => {
    organization.created_at = new Date(organization.created_at).toLocaleString(
      undefined,
      localeDateTimeOptions
    );
    return organization;
  });
}
</script>
