<script lang="ts">
export default {
  computed: {
    room: {
      get() {
        return window.location.href.split("#").pop().startsWith("http");
      },
    },
    username: {
      get() {
        return window.currentUser ? window.currentUser.user : null;
      },
      set(user) {
        window.currentUser = {
          user: user,
        };
      },
    },
  },
  data() {
    return {
      dialog: true,
      user: null,
    };
  },
};
</script>

<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="500">
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">Username</v-card-title>
        <v-card-actions>
          <v-container>
            <v-row justify="center">
              <v-col>
                <v-card-text>What is your Name? </v-card-text>
                <input
                  v-model="username"
                  type="text"
                  style="background: white"
                />
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
