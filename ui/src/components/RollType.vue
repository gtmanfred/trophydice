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
  <div class="rolltype">
    <div>
      <button class="btn" v-html="name"></button>
    </div>
  </div>
</template>
