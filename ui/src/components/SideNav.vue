<script setup lang="ts">
import RollType from "./RollType.vue";
import client from "../swagger";
</script>

<script lang="ts">
export default {
  mounted() {
    client.then((cli) => {
      console.log(cli)
      for (const endpoint in cli.apis.rolls) {
        console.log(cli.apis.rolls[endpoint].arguments);
        /*
        this.endpoints.push({
          path: cli.apis.rolls[endpoint],
          name: endpoint.split("/").pop(),
        });
        */
      }
    });
  },
  data() {
    return {
      endpoints: [],
    };
  },
};
</script>

<style scoped>
div.sidenav {
  display: flex;
  flex-direction: row;
  justify-content: left;
}
</style>

<template>
  <div class="sidenav">
    <RollType
      v-for="endpoint in endpoints"
      :key="endpoint"
      :endpoint="endpoint.path"
      :name="endpoint.name"
    />
  </div>
</template>
