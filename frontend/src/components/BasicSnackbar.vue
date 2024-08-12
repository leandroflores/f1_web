<template>
  <v-snackbar v-model="model" location="bottom" :color="color">
    {{ message }}
    <template v-slot:actions>
      <v-btn variant="text" @click="model = false" icon="mdi-close"> </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup lang="ts">
const model = defineModel<boolean>({ required: true }); // eslint-disable-line

const props = defineProps<{
  color: string;
  message: string;
}>();
</script>
