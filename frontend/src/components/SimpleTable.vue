<template>
  <div class="px-4 py-2 d-flex justify-space-between">
    <v-combobox
      append-inner-icon="mdi-magnify"
      label="Filtrar"
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
  </div>
  <v-data-table
    class="simple-table"
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
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon
        icon="mdi-file"
        class="me-2"
        :data-tippy-content="tippyDetails"
        color="primary"
        @click="openDetails(item)"
      >
        <v-tooltip activator="parent" location="start">Teste</v-tooltip>
      </v-icon>
      <v-icon
        icon="mdi-cached"
        class="me-2"
        :data-tippy-content="tippyDetails"
        color="primary"
        @click="newSearch(item)"
      >
      </v-icon>
    </template>
  </v-data-table>
</template>

<script setup lang="ts">
import axios from "axios";
import { computed, onBeforeMount, ref, useSlots } from "vue";
import tippy from "tippy.js";
import { useRouter } from "vue-router";
import { useSnackbar } from "@/store";

export interface Messages {
  unexpectedError: string;
}

interface Props {
  messages: Messages;
  urlBase: string;
  headers: any[];
  itemsProcess?: (items: any[]) => any[];
}

const router = useRouter();
const props = withDefaults(defineProps<Props>(), {});

const { showSnackbar } = useSnackbar();

const tippyDetails = "Detalhes";
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

function newSearch(item: any) {
  router.push({ name: "search", query: { document: item.document } });
}

function openDetails(item: any) {
  router.push({ name: "serch_report", params: { search_id: item.id } });
}
</script>

<style scoped lang="scss">
.simple-table::v-deep tbody tr:hover {
  background-color: rgba(0, 0, 0, 0.02);
}
</style>
