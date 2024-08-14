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
      :items-process="driversProcess"
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
          label="Identificador"
          name="identifier"
          :error-messages="identifierError"
          v-model="createFormData.identifier"
          validate-on="blur"
          :rules="[required]"
          autofocus
          ref="identifierInput"
        ></v-text-field>
        <v-text-field
          label="Código"
          name="code"
          v-model="createFormData.code"
          validate-on="blur"
          :rules="[required]"
          autofocus
        ></v-text-field>
        <v-text-field
          label="Nome"
          name="first_name"
          v-model="createFormData.first_name"
          validate-on="blur"
          :rules="[required]"
          autofocus
        ></v-text-field>
        <v-text-field
          label="Sobrenome"
          name="last_name"
          v-model="createFormData.last_name"
          validate-on="blur"
          :rules="[required]"
          autofocus
        ></v-text-field>
        <v-text-field
          label="Data de Nascimento"
          name="birth_date"
          v-model="createFormData.birth_date"
          validate-on="blur"
          :rules="[required]"
          autofocus
        ></v-text-field>
        <v-text-field
          label="Nacionalidade"
          name="country"
          v-model="createFormData.country"
          validate-on="blur"
          :rules="[required]"
          autofocus
        ></v-text-field>
        <v-text-field
          label="URL"
          name="url"
          v-model="createFormData.url"
          validate-on="blur"
          autofocus
        ></v-text-field>
      </template>

      <template v-slot:editForm>
        <v-text-field
          label="Identificador"
          name="identifier"
          :error-messages="identifierError"
          v-model="createFormData.identifier"
          validate-on="blur"
          :rules="[required]"
          autofocus
          ref="identifierInput"
        ></v-text-field>
        <v-text-field
          label="Código"
          name="code"
          v-model="createFormData.code"
          validate-on="blur"
          :rules="[required]"
          autofocus
        ></v-text-field>
        <v-text-field
          label="Nome"
          name="first_name"
          v-model="createFormData.first_name"
          validate-on="blur"
          :rules="[required]"
          autofocus
        ></v-text-field>
        <v-text-field
          label="Sobrenome"
          name="last_name"
          v-model="createFormData.last_name"
          validate-on="blur"
          :rules="[required]"
          autofocus
        ></v-text-field>
        <v-text-field
          label="Data de Nascimento"
          name="birth_date"
          v-model="createFormData.birth_date"
          validate-on="blur"
          :rules="[required]"
          autofocus
        ></v-text-field>
        <v-text-field
          label="Nacionalidade"
          name="country"
          v-model="createFormData.country"
          validate-on="blur"
          :rules="[required]"
          autofocus
        ></v-text-field>
        <v-text-field
          label="URL"
          name="url"
          v-model="createFormData.url"
          validate-on="blur"
          autofocus
        ></v-text-field>
      </template>
    </CRUDTable>
  </v-container>
</template>

<script setup lang="ts">
import { AxiosError } from "axios";
import CRUDTable from "@/components/CRUDTable.vue";
import { localeDateOptions } from "@/consts";
import { reactive, ref } from "vue";
import { required } from "@/validators";
import { useLoadDrivers } from "@/composables/load-organizations";
import { watchOnce } from "@vueuse/core";

const defaultCreateFormData = {
  identifier: "",
  code: "",
  first_name: "",
  last_name: "",
  birth_date: "",
  country: "",
  url: "",
};
const defaultEditFormData = {
  identifier: "",
  code: "",
  first_name: "",
  last_name: "",
  birth_date: "",
  country: "",
  url: "",
};
const createFormData = reactive({ ...defaultCreateFormData });
const editFormData = reactive({ ...defaultEditFormData });
const urlBase = "/drivers";
const crudMsgs = {
  unexpectedError:
    "Erro inesperado. Tente novamente ou entre em contato com o suporte.",
  createSuccess: "Piloto criado com sucesso!",
  editSuccess: "Piloto editado com sucesso!",
};
const createConfig = {
  btnText: "Novo Piloto ",
  btnIcon: "mdi-plus",
  formTitle: "Novo Piloto",
  formIcon: "mdi-briefcase-plus",
  submitText: "Salvar",
  formDataDefault: defaultCreateFormData,
  handleCreateError: checkExistingIdentifier,
};
const editConfig = {
  btnText: "Editar Empresa",
  formTitle: "Editando Empresa",
  formIcon: "mdi-briefcase-edit",
  submitText: "Salvar",
  formDataDefault: defaultEditFormData,
  handleEditError: checkExistingIdentifier,
};

const tableHeaders = [
  {
    title: "ID",
    key: "id",
  },
  {
    title: "Nome",
    key: "first_name",
  },
  {
    title: "Sobrenome",
    key: "last_name",
  },
  {
    title: "País",
    key: "country",
  },
  {
    title: "Nascimento",
    key: "birth_date",
  },
  {
    title: "Ações",
    key: "actions",
    sortable: false,
    align: "end",
  },
];

const identifierError = ref("");
const identifierInput = ref();
const existingNameMsg = "Piloto com este identificar já existe";

function checkExistingIdentifier(err: AxiosError<any, any>) {
  if (err.response?.status === 409) {
    identifierError.value = existingNameMsg;
    identifierInput.value.focus();
    watchOnce(
      () => createFormData.identifier || editFormData.identifier,
      () => (identifierError.value = "")
    );
    return true;
  }
  return false;
}

const { drivers, loadingDrivers, load: loadDrivers } = useLoadDrivers();

function driversProcess(drivers: any[]) {
  return drivers.map((driver) => {
    driver.birth_date = new Date(driver.birth_date).toLocaleString(
      undefined,
      localeDateOptions
    );
    // driver.organization_id = driver.organization?.id;
    return driver;
  });
}
async function loadAll() {
  await Promise.all([loadDrivers()]);
}
</script>
