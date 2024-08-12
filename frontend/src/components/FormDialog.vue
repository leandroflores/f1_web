<template>
  <v-dialog
    :modelValue="open"
    max-width="600"
    transition="dialog-transition"
    :persistent="true"
    retain-focus
    @keyup.esc="closeDialog"
  >
    <v-card :title="title">
      <template v-slot:prepend>
        <v-avatar v-if="titleIcon">
          <v-icon color="primary" :icon="titleIcon"></v-icon>
        </v-avatar>
      </template>
      <v-btn
        icon="mdi-close"
        tabindex="-1"
        variant="text"
        @click="closeDialog"
        style="position: absolute; right: 0; top: 0; margin: 0.5rem"
      >
      </v-btn>
      <v-form v-model="formValid" @submit.prevent="submitForm">
        <v-card-text>
          <slot></slot>
          <p class="text-error">{{ formError }}</p>
        </v-card-text>
        <v-card-actions>
          <v-btn
            :loading="loadingSubmit"
            type="submit"
            size="large"
            variant="tonal"
            block
            prepend-icon="mdi-content-save"
            color="primary"
            :text="submitText"
          ></v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits(["close"]);

const props = defineProps<{
  title: string;
  titleIcon: string;
  submitText: string;
  open: boolean;
  formError?: string;
  submit: () => Promise<any>;
}>();

const loadingSubmit = ref(false);
const formValid = ref(false);

function closeDialog() {
  emit("close");
}

async function submitForm() {
  if (!formValid.value) return;
  loadingSubmit.value = true;
  await props.submit();
  loadingSubmit.value = false;
}
</script>
