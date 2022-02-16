<script setup lang="ts">
import RollCard from "./RollCards.vue";
import socket from "../socket";
</script>

<script lang="ts">
export default {
  mounted() {
    socket.on("v1/risk", (data) => {
      this.rolls.push(data);
    });
  },
  data() {
    return {
      rolls: [],
    };
  },
};
</script>

<template>
  <div>
    <RollCard
      v-for="roll in rolls"
      :key="roll.id"
      :message="roll.message"
      :dice="roll.dice"
    />
  </div>
</template>
