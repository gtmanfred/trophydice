import VueSocketIOExt from "vue-socket.io-extended";
import { createApp } from "vue";
import App from "./App.vue";
import socket from "./socket";
import axios from "axios";
import VueAxios from "vue-axios";
import client from "./swagger";
import vuetify from "./plugins/vuetify";
import VueSimpleAlert from "vue3-simple-alert";

const app = createApp(App);

app.config.globalProperties.socket = socket;
app.config.globalProperties.client = client;

app.use(VueSocketIOExt, socket);
app.use(VueAxios, axios);
app.use(vuetify);
app.use(VueSimpleAlert);
app.mount("#app");
