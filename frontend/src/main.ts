import { createApp } from "vue";
import { createPinia } from "pinia";
import resetStore from "./plugins/reset-store";
import App from "./App.vue";
import router from "./router";

// Vuetify
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import vuetifyPlugin from "@/plugins/vuetify";

// Tippy JS
import "tippy.js/dist/tippy.css";

// Directives
import simplemaskmoney from "./directives/simplemaskmoney";

// dayjs
import relativeTime from "dayjs/plugin/relativeTime";
import updateLocale from "dayjs/plugin/updateLocale";
import "dayjs/locale/pt-br";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
dayjs.extend(utc);
dayjs.extend(updateLocale);
dayjs.extend(relativeTime);
dayjs.locale("pt-BR");
dayjs.updateLocale("pt-BR", {
  relativeTime: {
    future: "em %s",
    past: "%s atrás",
    s: "poucos segundos",
    m: "um minuto",
    mm: "%d minutos",
    h: "uma hora",
    hh: "%d horas",
    d: "um dia",
    dd: "%d dias",
    M: "um mês",
    MM: "%d meses",
    y: "um ano",
    yy: "%d anos",
  },
});

import { Vue3SimpleHtml2pdf } from "vue3-simple-html2pdf";

const pinia = createPinia();
pinia.use(resetStore);
const app = createApp(App);

// Plugins
app.use(pinia);
app.use(router);
app.use(vuetifyPlugin);
app.use(Vue3SimpleHtml2pdf);

app.directive("simple-mask-money", simplemaskmoney);

app.mount("#app");
