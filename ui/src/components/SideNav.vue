<script setup lang="ts">
import RollType from "./RollType.vue";
import NickList from "./NickList.vue";
import GenericRoll from "./GenericRoll.vue";
import KoFiButton from "@linusborg/vue-ko-fi-button";
</script>

<script lang="ts">
export default {
  props: ["drawer"],
  methods: {
    toggleDrawer() {
      if (window.innerWidth <= 760) {
        this.state = !this.state;
      }
    },
  },
  mounted() {
    console.log(this.state);
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
      state: window.innerWidth > 760,
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
  <v-navigation-drawer temporary v-model="state" width="300">
    <v-expansion-panels accordian>
      <RollType
        v-for="endpoint in endpoints"
        :key="endpoint.name"
        :endpoint="endpoint.endpoint"
        :name="endpoint.name"
        :path="endpoint.path"
        v-on:drawer-toggle="toggleDrawer()"
      />
      <GenericRoll v-on:drawer-toggle="toggleDrawer()" />
    </v-expansion-panels>
    <NickList />
    <KoFiButton username="gtmanfred" color="#323842" title="Support Me" />
  </v-navigation-drawer>
</template>
