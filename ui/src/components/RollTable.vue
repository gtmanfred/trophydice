<script setup lang="ts">
import { parseStringStyle } from "@vue/shared";
import RollCard from "./RollCards.vue";
</script>

<script lang="ts">
export default {
  mounted() {
    this.emitter.$on("roll", (roll) => {
      this.rolls[roll.uid] = roll;
    });
    this.getRollList();
    setInterval(this.getRollList, 5000);
  },
  methods: {
    getRollList() {
      this.client.then(client => {
        client.apis.room.get_room({
          room_uid: this.$route.params.room, 
          seq_id: this.seq_id
        }).then(resp => {
          this.seq_id = resp.obj.seq_id;
          for (let result of resp.obj.results) {
            this.rolls[result.uid] = result;
          };
        });
      });
    },
    updateAndScroll(message) {
      this.rolls[message.uid] = message;
    },
    reversedRolls() {
      return Object.values(this.rolls).reverse();
    },
  },
  data() {
    return {
      rolls: {},
      seq_id: 0,
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
      v-for="roll in reversedRolls()"
      :key="roll.id"
      :message="roll.message"
      :dice="roll.dice"
    />
  </v-sheet>
</template>
