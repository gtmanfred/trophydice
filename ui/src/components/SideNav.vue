<script setup lang="ts">
import RollType from "./RollType.vue";
</script>

<script lang="ts">
export default {
  props: ["drawer"],
  mounted() {
    this.client.then((cli) => {
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
  watch: {
    drawer: function () {
      this.state = !this.state;
    },
  },
  data() {
    return {
      endpoints: [],
      model: 1,
      state: null,
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
  <v-navigation-drawer v-model="state" temporary>
    <v-expansion-panels accordian>
      <RollType
        v-for="endpoint in endpoints"
        :key="endpoint.name"
        :endpoint="endpoint.endpoint"
        :name="endpoint.name"
        :path="endpoint.path"
        v-on:drawer-toggle="state = !state"
      />
    </v-expansion-panels>
  </v-navigation-drawer>
</template>
