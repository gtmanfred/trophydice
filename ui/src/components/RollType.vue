<script lang="ts">
export default {
  props: ["endpoint", "name", "path"],
  computed: {
    room: {
      get() {
        return window.location.href.split("#").pop();
      },
    },
  },
  mounted() {
    for (const param in this.endpoint.get.parameters) {
      if (this.endpoint.get.parameters[param].in === "query") {
        this.params.push(this.endpoint.get.parameters[param].name);
      }
    }
  },
  methods: {
    increment(index) {
      this.diceNums[index]++;
    },
    decrement(index) {
      if (this.diceNums[index] == 0) {
        return;
      }
      this.diceNums[index]--;
    },
    submitForm() {
      let payload = {};
      for (let index = 0; index < this.params.length; index++) {
        payload[this.params[index]] = this.diceNums[index];
      }
      let config = {
        params: payload,
        headers: {
          "x-room": this.room,
          "x-user-name": window.currentUser ? window.currentUser.user : "Guest",
        },
      };
      this.axios
        .get(`${window.location.origin}${this.path}`, config)
        .then(() => {
          this.$emit("drawer-toggle");
          this.diceNums = [0, 0];
        });
    },
  },
  data() {
    return {
      params: [],
      diceNums: [0, 0],
    };
  },
};
</script>

<template>
  <v-expansion-panel>
    <v-expansion-panel-title>{{ name }}</v-expansion-panel-title>
    <v-expansion-panel-text>
      <v-container v-for="(param, index) in params" v-bind:key="param">
        <v-row justify="center">
          <v-chip>{{ param }} {{ diceNums[index] }}</v-chip>
          <v-btn @click="decrement(index)" class="changer">-</v-btn>
          <v-btn @click="increment(index)" color="grey--darken-2">+</v-btn>
        </v-row>
      </v-container>
      <v-container>
        <v-row justify="center">
          <v-btn @click="submitForm" color="red" x-small>Roll</v-btn>
        </v-row>
      </v-container>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>
