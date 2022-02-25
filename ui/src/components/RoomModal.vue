<script setup lang="ts">
import Str from "@supercharge/strings";
</script>
<script lang="ts">
export default {
  data() {
    return {
      room: null,
      dialog: location.hash.split("#").pop() ? false : true,
    };
  },
  methods: {
    redirectToRoom() {
      location.hash = `#${this.room}`;
      this.socket.emit("join_room", { room_name: this.room });
      this.dialog = false;
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
        <v-row justify="center">
          <v-card-text>
            <v-col>
              <v-card-text>Create a room?</v-card-text>
            </v-col>
          </v-card-text>
          <v-card-actions>
            <v-col>
              <v-btn text @click="createRoom()">Create.</v-btn>
            </v-col>
          </v-card-actions>
        </v-row>
      </v-card>
    </v-dialog>
  </div>
</template>
