import { RouteRecordRaw } from "vue-router";
import LoginView from "@/modules/users/LoginView.vue";
import NavbarView from "@/components/NavbarView.vue";
import AdminHomeView from "@/modules/admin/AdminHomeView.vue";
import UsersView from "@/modules/users/UsersView.vue";
import CompaniesView from "@/modules/users/CompaniesView.vue";
import OrganizationsView from "@/modules/users/OrganizationsView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "",
    name: "home",
    component: NavbarView,
    redirect: "usuarios",
    children: [
      {
        path: "usuarios",
        name: "users",
        component: UsersView,
        meta: {
          title: "Usuários | Formula 1",
        },
      },
      {
        path: "organizacoes",
        name: "organizations",
        component: OrganizationsView,
        meta: {
          title: "Organizações | Formula 1",
        },
      },
      {
        path: "empresas",
        name: "companies",
        component: CompaniesView,
        meta: {
          title: "Empresas | Formula 1",
        },
      },
    ],
  },
  {
    path: "/admin",
    name: "admin",
    component: AdminHomeView,
    meta: {
      title: "Admin | Formula 1",
    },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: {
      title: "Formula 1 - Login",
    },
    props: (route) => ({ ...route.query, ...route.params }),
  },
];

export default routes;
