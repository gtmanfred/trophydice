import VueSocketIOExt from "vue-socket.io-extended";
import { createApp } from "vue";
import App from "./App.vue";
import socket from "./socket";

const app = createApp(App);

app.mount("#app");
app.use(VueSocketIOExt, socket);
