<script setup lang="ts">
import RollTable from "./components/RollTable.vue";
import SideNav from "./components/SideNav.vue";
import RoomModal from "./components/RoomModal.vue";
import UserModal from "./components/UserModal.vue";
</script>

<script lang="ts">
export default {
  methods: {
    pingConnection() {
      if (!this.socket.connected) {
        this.socket.io.reconnect();
        return;
      }
    },
    connect() {
      this.socket.on("connect", () => {
        console.log("Connected to websocket!");
        console.log(`Join room: ${this.$route.params.room}`);
        this.socket.emit("join_room", { room_name: this.$route.params.room });
      });
    },
  },
  components: {
    RollTable,
    SideNav,
    RoomModal,
    UserModal,
  },
  mounted() {
    this.connect();
    setInterval(this.pingConnection, 1000);
  },
  data() {
    return {
      drawer: true,
    };
  },
};
</script>

<template>
  <v-app>
    <v-sheet
      class="overflow-hidden"
      style="position: relative; height: 100vh; margin: auto"
    >
      <header style="margin: 1rem">
        <v-row justify="center">
          <v-col></v-col>
          <v-col>
            <img
              alt="Trophy logo"
              class="logo"
              src="./assets/logo.svg"
              width="100"
              height="100"
            />
          </v-col>
          <v-col justify="right">
            <v-btn color="pink" @click.stop="drawer = !drawer">Rolls</v-btn>
          </v-col>
        </v-row>
      </header>

      <v-main>
        <SideNav :drawer="drawer" />
        <RollTable />
        <UserModal />
        <RoomModal />
      </v-main>
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
