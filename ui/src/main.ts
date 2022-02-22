import VueSocketIOExt from "vue-socket.io-extended";
import { createApp } from "vue";
import App from "./App.vue";
import socket from "./socket";
import axios from "axios";
import VueAxios from "vue-axios";

const app = createApp(App);

app.mount("#app");
app.use(VueSocketIOExt, socket);
app.use(VueAxios, axios);
