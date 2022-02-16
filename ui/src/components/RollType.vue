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
  data() {
    return {
      params: [],
    };
  },
};
</script>

<template>
  <div id="side-nav" class="sidenav">
    <div>
      <button v-html="name"></button>
      <form v-bind:id="name">
      </form>
    </div>
  </div>
</template>
