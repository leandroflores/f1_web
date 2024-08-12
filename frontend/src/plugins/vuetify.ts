import { createVuetify } from "vuetify";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import { pt } from "vuetify/locale";

const formulaOneTheme = {
  dark: false,
  colors: {
    background: "#FFFFFF",
    surface: "#FFFFFF",
    primary: "#95A6B7",
    "primary-darken-1": "#283593",
    secondary: "#FF9800",
    "secondary-darken-1": "#EF6C00",
    error: "#E53935",
    info: "#1E88E5",
    success: "#43A047",
    warning: "#FB8C00",
    navbar: "#95A6B7",
  },
};

export default createVuetify({
  // Vuetify Icon Fonts: https://vuetifyjs.com/en/features/icon-fonts/
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: "formulaOneTheme",
    themes: {
      formulaOneTheme,
    },
  },
  locale: {
    locale: "pt",
    messages: { pt },
  },
  // defaults: {
  //   VTextField: {
  //     variant: "underlined",
  //   },
  // },
});
