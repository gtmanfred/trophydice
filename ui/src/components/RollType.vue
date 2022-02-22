<script lang="ts">
export default {
  props: ["endpoint", "name", "path"],
  computed: {
    room: {
      get() {
        return window.location.href.split("#").pop();
      },
    },
  },
  mounted() {
    for (const param in this.endpoint.get.parameters) {
      if (this.endpoint.get.parameters[param].in === "query") {
        this.params.push(this.endpoint.get.parameters[param].name);
      }
    }
  },
  methods: {
    submitForm() {
      let payload = {};
      for (let index = 0; index < this.params.length; index++) {
        payload[this.params[index]] = this.diceNums[index];
      }
      let config = {
        params: payload,
        headers: {
          "x-room": this.room,
        },
      };
      console.log(`${window.location.origin}${this.path}`);
      this.axios
        .get(`${window.location.origin}${this.path}`, config)
        .then((resp) => {
          console.log(resp);
        });
    },
  },
  data() {
    return {
      params: [],
      diceNums: [0, 0],
    };
  },
};
</script>

<template>
  <div class="rolltype">
    <div>
      <div v-for="(param, index) in params" v-bind:key="param">
        <p>{{ param }}</p>
        <input type="number" v-model="diceNums[index]" placeholder="0" />
      </div>
      <button @click="submitForm" class="btn" v-html="name"></button>
    </div>
  </div>
</template>
