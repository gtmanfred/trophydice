<script lang="ts">
export default {
  computed: {
    username: {
      get() {
        return window.currentUser ? window.currentUser.user : null;
      },
      set(user) {
        window.currentUser = {
          user: user,
        };
        this.socket.emit("set_nick", { nick: user });
      },
    },
  },
  data() {
    return {
      dialog: true,
    };
  },
};
</script>

<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="20vw">
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">Display Name</v-card-title>
        <v-card-actions>
          <v-container>
            <v-row justify="center">
              <v-col>
                <v-card-text justify="center">
                  <v-text-field label="What is your name?" v-model="username" />
                </v-card-text>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-btn text @click="dialog = false">save</v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
