import VueSocketIOExt from "vue-socket.io-extended";
import { createApp } from "vue";
import App from "./App.vue";
import socket from "./socket";
import axios from "axios";
import VueAxios from "vue-axios";
import client from "./swagger";
import vuetify from "./plugins/vuetify";

const app = createApp(App);

app.config.globalProperties.socket = socket;
app.config.globalProperties.client = client;

app.use(VueSocketIOExt, socket).use(VueAxios, axios).use(vuetify).mount("#app");
