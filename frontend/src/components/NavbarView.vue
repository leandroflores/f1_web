<template>
  <v-app-bar color="navbar" class="justify-center">
    <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
    <v-app-bar-title
      style="cursor: pointer"
      @click="$router.push({ name: 'users' })"
      class="flex-0-0"
    >
      <v-img src="/static/assets/logo2.png" width="300"></v-img>
    </v-app-bar-title>
  </v-app-bar>
  <v-navigation-drawer v-model="drawer" temporary>
    <v-list>
      <v-list-item
        prepend-icon="mdi-account"
        :subtitle="store.userMe?.email"
        :title="store.userMe?.full_name"
      ></v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list nav>
      <v-list-item
        v-if="store.userMe?.is_admin"
        prepend-icon="mdi-badge-account-horizontal"
        title="Empresas"
        value="companies"
        @click="$router.push({ name: 'companies' })"
        active-color="primary"
      >
      </v-list-item>
      <v-list-item
        v-if="store.userMe?.is_master"
        prepend-icon="mdi-briefcase"
        title="Organizações"
        value="organizations"
        @click="$router.push({ name: 'organizations' })"
        active-color="primary"
      >
      </v-list-item>
      <v-list-item
        v-if="store.userMe?.is_admin"
        prepend-icon="mdi-account-group"
        title="Usuários"
        value="users"
        @click="$router.push({ name: 'users' })"
      ></v-list-item>
      <!--<v-list-item
        v-if="store.userMe?.is_admin"
        prepend-icon="mdi-shield-account"
        title="Painel Admin"
        value="admin"
        @click="$router.push({ name: 'admin.home' })"
      ></v-list-item> -->
    </v-list>

    <template v-slot:append>
      <v-list>
        <v-list-item
          title="Sair da conta"
          value="sair"
          prepend-icon="mdi-logout"
          variant="tonal"
          @click="logout"
        >
        </v-list-item>
      </v-list>
    </template>
  </v-navigation-drawer>
  <v-main style="height: 100%" class="bg-grey-lighten-3">
    <router-view />
  </v-main>
</template>

<script setup lang="ts">
import { useUsersStore } from "@/modules/users/store";
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";

const store = useUsersStore();
const router = useRouter();

const drawer = ref(false);

function logout() {
  axios.post("/logout").finally(() => {
    store.logout();
    router.push({ name: "login" });
  });
}
</script>

<style scoped lang="scss">
.v-application {
  font-family: "Roboto", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.v-app-bar::v-deep .v-toolbar__content {
  max-width: 1280px;
  margin: auto;
}
</style>
