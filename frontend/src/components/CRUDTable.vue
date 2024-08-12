<template>
  <div class="px-4 py-2 d-flex justify-space-between">
    <v-combobox
      append-inner-icon="mdi-magnify"
      label="Pesquisar"
      name="search"
      density="compact"
      v-model="search"
      hide-details
      single-line
      multiple
      chips
      autocomplete="off"
      style="max-width: 400px"
    ></v-combobox>
    <v-btn
      v-if="createConfig"
      :text="createConfig.btnText"
      variant="tonal"
      color="primary"
      :prepend-icon="createConfig.btnIcon"
      @click="initCreate"
    ></v-btn>
  </div>
  <v-data-table
    class="crud-table"
    :items="items"
    item-value="id"
    :headers="headers"
    :loading="loading"
    :search="searchQuery"
    :custom-filter="customFilter"
  >
    <template v-for="slot in Object.keys(slots)" v-slot:[slot]="{ item }">
      <slot :name="slot" :item="item"></slot>
    </template>
    <template v-if="editConfig" v-slot:[`item.actions`]="{ item }">
      <v-icon
        icon="mdi-pencil"
        class="me-2"
        :data-tippy-content="editConfig.btnText"
        color="primary"
        @click="initEdit(item)"
      >
      </v-icon>
    </template>
  </v-data-table>

  <FormDialog
    v-if="createConfig"
    :title="createConfig.formTitle"
    :titleIcon="createConfig.formIcon"
    :submitText="createConfig.submitText"
    :open="openCreateForm"
    :form-error="formError"
    :submit="submitCreate"
    @close="closeCreate"
  >
    <slot name="createForm"></slot>
  </FormDialog>

  <FormDialog
    v-if="editConfig"
    :title="editConfig.formTitle"
    :titleIcon="editConfig.formIcon"
    :submitText="editConfig.submitText"
    :open="openEditForm"
    :form-error="formError"
    :submit="submitEdit"
    @close="closeEdit"
  >
    <slot name="editForm"></slot>
  </FormDialog>
</template>

<script setup lang="ts">
import { useSnackbar } from "@/store";
import { watchOnce } from "@vueuse/core";
import axios, { AxiosError } from "axios";
import tippy from "tippy.js";
import { computed, onBeforeMount, ref, useSlots } from "vue";
import FormDialog from "./FormDialog.vue";

export interface Messages {
  unexpectedError: string;
  createSuccess: string;
  editSuccess: string;
}

export interface CreateConfig {
  btnText: string;
  btnIcon: string;
  formTitle: string;
  formIcon: string;
  submitText: string;
  formDataDefault: any;
  handleCreateError?: (err: AxiosError<any, any>) => boolean;
}

export interface EditConfig {
  btnText: string;
  formTitle: string;
  formIcon: string;
  submitText: string;
  formDataDefault: any;
  handleEditError?: (err: AxiosError<any, any>) => boolean;
}

interface Props {
  messages: Messages;
  urlBase: string;
  headers: any[];
  createConfig?: CreateConfig;
  editConfig?: EditConfig;
  itemsProcess?: (items: any[]) => any[];
  createProcess?: (data: any) => any;
  editProcess?: (data: any) => any;
}
const props = withDefaults(defineProps<Props>(), {});

// eslint-disable-next-line
const formError = defineModel("formError", {
  required: false,
  type: String,
  default: "",
});
// eslint-disable-next-line
const createFormData = defineModel("createFormData", {
  required: true,
  type: Object,
});
// eslint-disable-next-line
const editFormData = defineModel("editFormData", {
  required: true,
  type: Object,
});

const { showSnackbar } = useSnackbar();

const emit = defineEmits<{
  (e: "createOpened"): void;
  (e: "editOpened", item: any): void;
}>();

const slots = useSlots();
const items = ref<any[]>([]);
const search = ref<string[]>([]);
const loading = ref(false);
const searchQuery = computed(() => {
  return search.value.join(",");
});

onBeforeMount(() => {
  getItems();
});

function customFilter(
  value: string | number,
  query: string,
  item?: any
): boolean | number | [number, number] | [number, number][] {
  if (typeof value === "number") value = value.toString();

  const queries = query
    .trim()
    .split(",")
    .filter((q) => q)
    .map((q) => q.trim().toLocaleLowerCase());

  return (
    value != null &&
    query != null &&
    typeof value === "string" &&
    queries.every((q) =>
      value
        .toLocaleLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .includes(q)
    )
  );
}

async function getItems() {
  try {
    loading.value = true;

    const res = await axios.get(props.urlBase);
    items.value = props.itemsProcess ? props.itemsProcess(res.data) : res.data;
    if (res.data.length != items.value.length) {
      throw new Error(
        "CRUDTable: 'itemsProcess' returned different number of items from response"
      );
    }
  } catch (err) {
    showSnackbar(props.messages.unexpectedError, "error");
    console.error(err);
  } finally {
    tippy("[data-tippy-content]", { arrow: false });
    loading.value = false;
  }
}

const openCreateForm = ref(false);

function initCreate() {
  openCreateForm.value = true;
  emit("createOpened");
}

async function submitCreate() {
  try {
    await axios.post(props.urlBase, createFormData.value);
    closeCreate();
    showSnackbar(props.messages.createSuccess, "success");
    getItems();
  } catch (err) {
    handleSubmitError(err, props.createConfig?.handleCreateError);
  }
}

function closeCreate() {
  formError.value = "";
  openCreateForm.value = false;
  resetCreateForm();
}

function resetCreateForm() {
  Object.assign(createFormData.value, props.createConfig?.formDataDefault);
}

const openEditForm = ref(false);
const editId = ref();

function initEdit(item: any) {
  for (const key in editFormData.value) {
    editFormData.value[key] = item[key];
  }
  openEditForm.value = true;
  editId.value = item.id;
  emit("editOpened", item);
}

async function submitEdit() {
  try {
    await axios.patch(`${props.urlBase}/${editId.value}`, editFormData.value);
    closeEdit();
    showSnackbar(props.messages.editSuccess, "success");
    getItems();
  } catch (err) {
    handleSubmitError(err, props.editConfig?.handleEditError);
  }
}

function handleSubmitError(
  err: any,
  handler: ((err: AxiosError<any, any>) => boolean) | undefined
) {
  if (axios.isAxiosError(err)) {
    const errorHandled = handler && handler(err);
    if (errorHandled) return;
  }
  formError.value = props.messages.unexpectedError;
  console.error(err);
  watchOnce(
    () => editFormData,
    () => (formError.value = "")
  );
}

function closeEdit() {
  formError.value = "";
  openEditForm.value = false;
  resetEditForm();
}

function resetEditForm() {
  editId.value = undefined;
  Object.assign(editFormData.value, props.editConfig?.formDataDefault);
}
</script>

<style scoped lang="scss">
.crud-table::v-deep tbody tr:hover {
  background-color: rgba(0, 0, 0, 0.02);
}
</style>
