<script setup lang="ts">
import Str from "@supercharge/strings";
</script>
<script lang="ts">
export default {
  data() {
    return {
      dialog: !this.$route.params.room,
    };
  },
  methods: {
    createRoom() {
      this.client.then(client => {
        client.apis.room.create_room().then(resp => {
          this.$router.push({ name: "room", params: { room: resp.obj.uid } });
        });
      });
      this.dialog = false;
    },
  },
};
</script>

<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="20vw">
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
              <v-btn text @click.stop="createRoom()" @click="dialog = false">Create.</v-btn>
            </v-col>
          </v-card-actions>
        </v-row>
      </v-card>
    </v-dialog>
  </div>
</template>
