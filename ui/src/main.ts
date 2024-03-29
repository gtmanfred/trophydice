import { createApp } from "vue";
import App from "./App.vue";
import client from "./swagger";
import vuetify from "./plugins/vuetify";
import emitter from "./eventBus";
import VueSimpleAlert from "vue3-simple-alert-next";
import { createRouter, createWebHistory } from "vue-router";

const prefix = process.env.NODE_ENV == "production" ? "/ui" : "";
const routes = [{ name: "room", path: `${prefix}/:room`, component: App }];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);

app.config.globalProperties.client = client;
app.config.globalProperties.emitter = emitter;

app.use(vuetify);
app.use(VueSimpleAlert);
app.use(router);

router.isReady().then(() => {
  app.mount("#app");
});
