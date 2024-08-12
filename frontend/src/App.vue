<template>
  <v-app>
    <router-view />

    <BasicSnackbar
      v-model="snackbar"
      :color="snackbarColor"
      :message="snackbarMsg"
    ></BasicSnackbar>
  </v-app>
</template>

<script setup lang="ts">
import BasicSnackbar from "@/components/BasicSnackbar.vue";
import { useSnackbar } from "@/store";
import { storeToRefs } from "pinia";

const { snackbar, snackbarColor, snackbarMsg } = storeToRefs(useSnackbar());
</script>

<style scoped lang="scss">
.v-application {
  font-family: "Roboto", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
