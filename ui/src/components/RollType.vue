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
    submitForm() {
      this.$parent.drawer = false;
      let payload = {};
      for (let index = 0; index < this.params.length; index++) {
        payload[this.params[index]] = this.diceNums[index];
      }
      let config = {
        params: payload,
        headers: {
          "x-room": this.room,
          "x-user-name": this.username,
        },
      };
      this.axios.get(`${window.location.origin}${this.path}`, config);
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
  <v-list-item>
    <v-list-item-content>
      <div v-for="(param, index) in params" v-bind:key="param">
        <label>{{ param }}</label>
        <v-btn @click="diceNums[index] += 1" rounded>+</v-btn>
        <v-btn @click="diceNums[index] -= 1" rounded>-</v-btn>
        <p>{{ diceNums[index] }}</p>
      </div>
      <v-btn @click="submitForm" class="btn">{{ name }}</v-btn>
    </v-list-item-content>
  </v-list-item>
</template>
