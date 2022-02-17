<script setup lang="ts">
import RollTable from "./components/RollTable.vue";
import SideNav from "./components/SideNav.vue";
import socket from "./socket";
</script>

<script lang="ts">
export default {
  computed: {
    room: {
      get() {
        return window.location.href.split("#").pop();
      },
    },
  },
  mounted() {
    socket.on("connect", () => {
      console.log("Connected to websocket!");
      console.log(`Join room: ${this.room}`);
      socket.emit("join_room", { room_name: this.room });
    });
  },
};
</script>

<template>
  <header>
    <img
      alt="Trophy logo"
      class="logo"
      src="./assets/logo.svg"
      width="125"
      height="125"
    />
  </header>

  <main>
    <RollTable />
    <SideNav />
  </main>
</template>

<style>
@import "./assets/base.css";

#app {
  max-width: 100vw;
  margin: 0 auto;
  padding: 2rem;
  font-weight: normal;
}

header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: auto;
  margin-bottom: 30px;
}
</style>
