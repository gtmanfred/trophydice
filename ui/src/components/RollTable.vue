<script setup lang="ts">
import { parseStringStyle } from "@vue/shared";
import RollCard from "./RollCards.vue";
</script>

<script lang="ts">
export default {
  mounted() {
    this.client.then((client) => {
      for (const path in client.spec.paths) {
        const output = path.split("/");
        this.socket.on(`${output[2]}/${output[3]}`, this.updateAndScroll);
      }
    });
  },
  methods: {
    updateAndScroll(message) {
      this.rolls.unshift(message);
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
#rolltable {
  height: 85vh;
  width: 100vw;
  overflow-y: scroll;
  text-align: center;
}
::-webkit-scrollbar {
  width: 0; /* Remove scrollbar space */
  background: transparent; /* Optional: just make scrollbar invisible */
}
</style>

<template>
  <v-sheet id="rolltable" class="rolls">
    <RollCard
      v-for="roll in rolls"
      :key="roll.id"
      :message="roll.message"
      :dice="roll.dice"
    />
  </v-sheet>
</template>
