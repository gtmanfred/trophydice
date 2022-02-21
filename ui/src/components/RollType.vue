<script setup lang="ts">
import client from "../swagger";
</script>

<script lang="ts">
export default {
  props: ["endpoint", "name"],
  mounted() {
    let params = [];
    for (const param in this.endpoint.get.parameters) {
      if (this.endpoint.get.parameters[param].in === "query") {
        params.push(this.endpoint.get.parameters[param].name);
      }
    }
  },
  methods: {
    rollDice() {
      let payload = {};
      for (const param in this.params) {
        payload[param] = Math.ceil(Math.random() * 5);
      }
      client;
    },
  },
  data() {
    return {
      params: [],
    };
  },
};
</script>

<template>
  <div class="rolltype">
    <div>
      <button class="btn" v-html="name"></button>
    </div>
  </div>
</template>
