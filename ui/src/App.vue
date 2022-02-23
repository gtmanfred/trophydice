<script setup lang="ts">
import RollTable from "./components/RollTable.vue";
import SideNav from "./components/SideNav.vue";
import RoomModal from "./components/RoomModal.vue";
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
    this.socket.on("connect", () => {
      console.log("Connected to websocket!");
      console.log(`Join room: ${this.room}`);
      this.socket.emit("join_room", { room_name: this.room });
    });
  },
  data() {
    return {
      drawer: false,
    };
  },
};
</script>

<template>
  <v-app>
    <v-sheet
      class="overflow-hidden"
      style="position: relative; display: float; height: 100vh; margin: auto"
    >
      <header>
        <v-btn color="pink" dark @click.stop="drawer = !drawer">Rolls</v-btn>
        <img
          alt="Trophy logo"
          class="logo"
          src="./assets/logo.svg"
          width="125"
          height="125"
        />
      </header>

      <main>
        <SideNav :drawer="drawer" />
        <RoomModal />
        <RollTable />
      </main>
    </v-sheet>
  </v-app>
</template>

<style>
@import "./assets/base.css";

#app {
  max-width: 100vw;
  margin: 0 auto;
  padding: 0;
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
