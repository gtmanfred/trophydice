<script setup lang="ts">
import RollType from "./RollType.vue";
import client from "../swagger";
</script>

<script lang="ts">
export default {
  mounted() {
    client.then((cli) => {
      for (const endpoint in cli.spec.paths) {
        if (cli.spec.paths[endpoint].get.tags) {
          this.endpoints.push({
            endpoint: cli.spec.paths[endpoint],
            name: endpoint.split("/").pop(),
            path: endpoint,
          });
        }
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
  flex-direction: column;
  justify-content: left;
}
</style>

<template>
  <div class="sidenav">
    <RollType
      v-for="endpoint in endpoints"
      :key="endpoint"
      :endpoint="endpoint.endpoint"
      :name="endpoint.name"
      :path="endpoint.path"
    />
  </div>
</template>
