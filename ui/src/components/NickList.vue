<script start>
export default {
  methods: {
    getNickList() {
      if (window.currentUser) {
        this.socket.emit("get_nicklist", { room: this.$route.params.room });
      }
    },
  },
  mounted() {
    this.socket.on("nicklist", (data) => {
      this.nicklist = data["nicks"];
    });
    setInterval(this.getNickList, 1000);
  },
  data() {
    return {
      nicklist: [],
    };
  },
};
</script>

<template>
  <v-list disabled>
    <v-list-subheader>Connected Users</v-list-subheader>
    <v-list-item v-for="nick in nicklist" :key="nick">
      <v-list-item-title>{{ nick }}</v-list-item-title>
    </v-list-item>
  </v-list>
</template>
