<script setup lang="ts">
import Str from "@supercharge/strings";
</script>
<script lang="ts">
export default {
  computed: {
    dialog: {
      get() {
        return window.location.href.split("#").pop().startsWith("http");
      },
    },
  },
  data() {
    return {
      room: null,
    };
  },
  methods: {
    redirectToRoom() {
      window.location.replace(`${window.location.href}#${this.room}`);
      window.location.reload();
    },
    createRoom() {
      this.room = Str.uuid();
      this.redirectToRoom();
    },
  },
};
</script>

<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="500">
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">Rooms</v-card-title>

        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-card-text>Create a room?</v-card-text>
          <v-btn color="primary" text @click="createRoom()">Create.</v-btn>
        </v-card-actions>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-card-text>Join a room?</v-card-text>
          <input v-model="room" type="text" style="background: white" />
          <v-btn color="primary" text @click="redirectToRoom()">Join.</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
