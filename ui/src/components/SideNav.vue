<script setup lang="ts">
import RollType from "./RollType.vue";
import client from "../swagger";
</script>

<script lang="ts">
export default {
  mounted() {
    client.then((cli) => {
      for (const endpoint in cli.spec.paths) {
        this.endpoints.push({
          path: cli.spec.paths[endpoint],
          name: endpoint.split("/").pop(),
        });
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
