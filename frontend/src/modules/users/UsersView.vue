<template>
  <v-container fluid class="d-flex">
    <v-card class="flex-1-1" title="Usuários">
      <template v-slot:prepend>
        <v-icon color="primary" icon="mdi-account"></v-icon>
      </template>
      <v-card-text>
        <CRUDTable
          v-model:create-form-data="createFormData"
          v-model:edit-form-data="editFormData"
          :url-base="urlBase"
          :messages="crudMsgs"
          :create-config="usersStore.canUsers ? createConfig : undefined"
          :edit-config="usersStore.canUsers ? editConfig : undefined"
          :headers="tableHeaders"
          :items-process="usersProcess"
          @create-opened="loadAll"
          @edit-opened="loadAll"
        >
          <template v-slot:[`item.is_active`]="{ item }">
            <v-icon
              :icon="item.is_active ? 'mdi-check' : 'mdi-cancel'"
              :color="item.is_active ? 'success' : 'error'"
            ></v-icon>
          </template>
          <template v-slot:[`item.is_admin`]="{ item }">
            <v-icon
              :icon="item.is_admin ? 'mdi-check' : 'mdi-cancel'"
              :color="item.is_admin ? 'success' : 'error'"
            ></v-icon>
          </template>
          <template v-slot:[`item.organizations`]="{ item }">
            <span v-if="item.organizations.length === 1">
              {{ item.organizations[0].name }}
            </span>
            <v-menu
              v-if="item.organizations.length > 1"
              :close-on-content-click="false"
            >
              <template v-slot:activator="{ props }">
                <v-chip value="org.id" v-bind="props"
                  >Ver {{ item.organizations.length }}</v-chip
                >
              </template>
              <v-list>
                <v-list-item v-for="org in item.organizations" :key="org.id">
                  <v-list-item-title>{{ org.name }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
          <template v-slot:createForm>
            <v-text-field
              ref="emailInput"
              type="email"
              label="Email"
              placeholder="seu@email.com"
              name="email"
              :error-messages="emailError"
              v-model="createFormData.email"
              validate-on="blur"
              :rules="[required, validateEmail]"
              autofocus
            ></v-text-field>
            <v-text-field
              :type="passwordPeek ? 'text' : 'password'"
              label="Senha"
              autocomplete="off"
              name="password"
              v-model="createFormData.password"
              validate-on="blur"
              :rules="[required, validatePassword]"
            >
              <template v-slot:append-inner>
                <v-btn
                  variant="plain"
                  density="compact"
                  :icon="passwordPeek ? 'mdi-eye' : 'mdi-eye-off'"
                  tabindex="-1"
                  @click="passwordPeek = !passwordPeek"
                ></v-btn>
              </template>
            </v-text-field>
            <v-text-field
              label="Nome Completo"
              name="full_name"
              v-model="createFormData.full_name"
              validate-on="blur"
              :rules="[required]"
            ></v-text-field>
            <v-autocomplete
              clearable
              label="Organização"
              auto-select-first
              name="organizacao"
              v-model="createFormData.organization_id"
              autocomplete="off"
              :items="organizations"
              :loading="loadingOrganizations"
              item-title="name"
              item-value="id"
              validate-on="blur"
              @update:model-value="
                loadCompaniesByOrganization(createFormData.organization_id)
              "
              :rules="[required]"
            ></v-autocomplete>
            <v-autocomplete
              clearable
              label="Empresas"
              auto-select-first
              name="companies"
              v-model="createFormData.companies_ids"
              autocomplete="off"
              :items="companies"
              item-title="name"
              item-value="id"
              validate-on="blur"
              multiple
              :rules="[requiredMultiple]"
            ></v-autocomplete>
            <v-checkbox
              label="Ativo"
              name="is_active"
              v-model="createFormData.is_active"
              hide-details
              single-line
            ></v-checkbox>
            <v-checkbox
              label="Administrador"
              name="is_admin"
              v-model="createFormData.is_admin"
              hide-details
              single-line
            ></v-checkbox>
          </template>

          <template v-slot:editForm>
            <v-text-field
              ref="emailInput"
              type="email"
              label="Email"
              placeholder="seu@email.com"
              name="email"
              :error-messages="emailError"
              v-model="editFormData.email"
              validate-on="blur"
              :rules="[required, validateEmail]"
              autofocus
            ></v-text-field>
            <v-text-field
              label="Nome Completo"
              name="full_name"
              v-model="editFormData.full_name"
              validate-on="blur"
              :rules="[required]"
            ></v-text-field>
            <v-autocomplete
              clearable
              label="Organização"
              auto-select-first
              name="organizations"
              v-model="editFormData.organization_id"
              autocomplete="off"
              :items="organizations"
              :loading="loadingOrganizations"
              item-title="name"
              item-value="id"
              validate-on="blur"
              @update:model-value="
                loadCompaniesByOrganization(editFormData.organization_id)
              "
              :rules="[required]"
            ></v-autocomplete>
            <v-autocomplete
              clearable
              label="Empresas"
              auto-select-first
              name="companies"
              v-model="editFormData.companies_ids"
              autocomplete="off"
              :items="companies"
              item-title="name"
              item-value="id"
              validate-on="blur"
              multiple
              :rules="[requiredMultiple]"
            ></v-autocomplete>
            <v-checkbox
              label="Ativo"
              name="is_active"
              v-model="editFormData.is_active"
              hide-details
              single-line
            ></v-checkbox>
            <v-checkbox
              label="Administrador"
              name="is_admin"
              v-model="editFormData.is_admin"
              hide-details
              single-line
            ></v-checkbox>
          </template>
        </CRUDTable>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import axios from "axios";
import CRUDTable from "@/components/CRUDTable.vue";
import { localeDateTimeOptions } from "@/consts";
import {
  required,
  requiredMultiple,
  validateEmail,
  validatePassword,
} from "@/validators";
import { watchOnce } from "@vueuse/core";
import { AxiosError } from "axios";
import { reactive, ref } from "vue";
import {
  useLoadCompanies,
  useLoadOrganizations,
} from "@/composables/load-organizations";
import { useUsersStore } from "./store";

const usersStore = useUsersStore();

const createFormDataDefault = {
  email: "",
  password: "",
  full_name: "",
  organization_id: undefined,
  companies_ids: [],
  is_active: true,
  is_admin: true,
};
const editFormDataDefault = {
  email: "",
  //password: undefined,
  full_name: "",
  organization_id: undefined,
  companies_ids: [],
  is_active: true,
  is_admin: true,
};
const createFormData = reactive({ ...createFormDataDefault });
const editFormData = reactive({ ...editFormDataDefault });
const urlBase = "/users";
const crudMsgs = {
  unexpectedError:
    "Erro inesperado. Tente novamente ou entre em contato com o suporte.",
  createSuccess: "Usuário criado com sucesso!",
  editSuccess: "Usuário editado com sucesso!",
};
const createConfig = {
  btnText: "Novo Usuário",
  btnIcon: "mdi-plus",
  formTitle: "Novo Usuário",
  formIcon: "mdi-briefcase-plus",
  submitText: "Salvar",
  formDataDefault: createFormDataDefault,
  handleCreateError: checkExistingEmail,
};
const editConfig = {
  btnText: "Editar Usuário",
  formTitle: "Editando Usuário",
  formIcon: "mdi-briefcase-edit",
  submitText: "Salvar",
  formDataDefault: editFormDataDefault,
  handleEditError: checkExistingEmail,
};
const tableHeaders = [
  {
    title: "Nome Completo",
    key: "full_name",
  },
  {
    title: "Email",
    key: "email",
  },
  {
    title: "Organização",
    key: "organization.name",
  },
  {
    title: "Ativo",
    key: "is_active",
  },
  {
    title: "Administrador",
    key: "is_admin",
  },
  {
    title: "Ações",
    key: "actions",
    sortable: false,
    align: "end",
  },
];

const passwordPeek = ref(false);
const emailError = ref("");
const emailInput = ref();
const companies = ref([]);

function loadCompaniesByOrganization(organizationId: any) {
  axios
    .get("/organizations/" + organizationId)
    .then((res) => {
      companies.value = res.data.companies;
      let ids = companies.value.map((objeto) => objeto.id);
      checkCompanies(ids, createFormData);
      checkCompanies(ids, editFormData);
    })
    .catch((err) => {
      companies.value = [];
    });
}

function checkCompanies(list: number[], form: object) {
  if (!form.companies_ids.every((elemento) => list.includes(elemento))) {
    form.companies_ids = [];
  }
}

function checkExistingEmail(err: AxiosError<any, any>) {
  if (err.response?.status === 409) {
    emailError.value = "Usuário com esse email já existe.";
    emailInput.value.focus();
    watchOnce(
      () => createFormData.email,
      () => (emailError.value = "")
    );
    return true;
  }
  return false;
}

function usersProcess(users: any[]) {
  return users.map((user: any) => {
    user.created_at = new Date(user.created_at).toLocaleString(
      undefined,
      localeDateTimeOptions
    );
    user.organization_id = user.organization?.id;
    user.companies_ids = user.companies.map((o: any) => o.id);
    return user;
  });
}

function loadCompanies() {
  let organizationId =
    createFormData.organization_id || editFormData.organization_id || 0;
  if (organizationId > 0) {
    loadCompaniesByOrganization(organizationId);
  }
}

const {
  organizations,
  loadingOrganizations,
  load: loadOrgs,
} = useLoadOrganizations();

async function loadAll() {
  await Promise.all([loadOrgs()]);
  loadCompanies();
}
</script>
