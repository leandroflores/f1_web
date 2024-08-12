<template>
  <v-main class="bg-grey-lighten-3" style="height: 100%">
    <div class="d-flex w-100 h-100 align-center justify-center">
      <v-card class="w-25">
        <v-card-item>
          <v-img src="/static/assets/logo_vert.png"></v-img>
        </v-card-item>
        <v-card-title>Entrar</v-card-title>
        <v-card-text>
          <v-form v-model="form" @submit.prevent="submitForm">
            <v-text-field
              type="email"
              label="Email"
              placeholder="seu@email.com"
              name="username"
              v-model="formData.username"
              validate-on="blur"
              :rules="[required, validateEmail]"
            ></v-text-field>
            <v-text-field
              :type="passwordPeek ? 'text' : 'password'"
              label="Senha"
              name="password"
              v-model="formData.password"
              validate-on="blur"
              :rules="[required]"
            >
              <template v-slot:append-inner>
                <v-btn
                  variant="plain"
                  density="compact"
                  :icon="passwordPeek ? 'mdi-eye' : 'mdi-eye-off'"
                  @click="passwordPeek = !passwordPeek"
                ></v-btn>
              </template>
            </v-text-field>
            <span class="text-error">{{ errorMessage }}</span>
            <v-btn
              type="submit"
              size="large"
              block
              color="primary"
              append-icon="mdi-login"
              class="mt-2"
              >Entrar</v-btn
            >
          </v-form>
        </v-card-text>
      </v-card>
    </div>
  </v-main>
</template>

<script setup lang="ts">
import { required, validateEmail } from "@/validators";
import axios from "axios";
import { reactive, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useUsersStore } from "./store";

const props = defineProps<{
  nextUrl?: string;
}>();

const router = useRouter();
const store = useUsersStore();

const passwordPeek = ref(false);
const form = ref(false);
const errorMessage = ref("");

const formData = reactive({
  username: "",
  password: "",
});

watch(formData, () => {
  errorMessage.value = "";
});
function submitForm() {
  if (!form.value) return;

  axios
    .post("/login", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then((res) => {
      if (props.nextUrl) {
        router.push(props.nextUrl);
        return;
      }
      router.push({ name: "home" });
    })
    .catch((err) => {
      if (err.response.status === 401) {
        errorMessage.value = "Email e/ou senha inválido(s).";
        return;
      }
      errorMessage.value =
        "Erro inesperado. Tente novamente ou entre em contato com o suporte.";
    });
}
</script>
