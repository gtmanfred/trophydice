<script setup lang="ts">
import RollCard from "./RollCards.vue";
</script>

<script lang="ts">
export default {
  mounted() {
    this.client.then((client) => {
      for (const path in client.spec.paths) {
        let output = path.split("/");
        this.socket.on(`${output[2]}/${output[3]}`, this.updateAndScroll);
      }
    });
  },
  methods: {
    updateAndScroll(message) {
      this.rolls.push(message);
      const timer = (ms) => new Promise((res) => setTimeout(res, ms));
      timer(100).then(() => {
        let tableDiv = document.getElementById("rolltable");
        tableDiv.scrollTop = tableDiv.scrollHeight - tableDiv.clientHeight;
      });
    },
  },
  data() {
    return {
      rolls: [],
    };
  },
};
</script>

<style>
div {
  scrollbar-width: none;
}
.rolls {
  height: 70vh;
  width: 50vw;
  overflow-y: scroll;
  text-align: center;
}
::-webkit-scrollbar {
  width: 0; /* Remove scrollbar space */
  background: transparent; /* Optional: just make scrollbar invisible */
}
</style>

<template>
  <v-sheet id="rolltable" class="rolls" style="width: 100vw">
    <RollCard
      v-for="roll in rolls"
      :key="roll.id"
      :message="roll.message"
      :dice="roll.dice"
    />
  </v-sheet>
</template>
