<script setup lang="ts">
import InputNumber from './InputNumber.vue';
</script>

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
    console.log(this.endpoint);
    for (const param in this.endpoint.get.parameters) {
      if (
        this.endpoint.get.parameters[param].in === "query" &&
        this.endpoint.get.parameters[param].schema.type === "integer"
      ) {
        this.params.push(this.endpoint.get.parameters[param].name);
      }
    }
  },
  methods: {
    changeNumber(index, event) {
      let value = parseInt(event);
      if (isNaN(parseInt(event))) {
        value = parseInt(event.target.value);
        if (isNaN(value)) return;
        this.diceNums[index] = value;
        return;
      }
      this.diceNums[index] = value;
    },
    submitForm() {
      const payload = {};
      for (let index = 0; index < this.params.length; index++) {
        payload[this.params[index]] = this.diceNums[index];
      }
      console.log(payload);
      const config = {
        params: payload,
        headers: {
          "x-room": this.room,
          "x-user-name": window.currentUser ? window.currentUser.user : "Guest",
        },
      };
      this.axios
        .get(`${window.location.origin}${this.path}`, config)
        .then(() => {
          this.$emit("drawer-toggle");
          this.diceNums = [0, 0];
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
  <v-expansion-panel>
    <v-expansion-panel-title>{{ name }}</v-expansion-panel-title>
    <v-expansion-panel-text>
      <v-form>
        <v-container v-for="(param, index) in params" v-bind:key="param">
          <v-row justify="center">
            <InputNumber
              :label="param"
              :value="diceNums[index]"
              v-on:input="(event) => changeNumber(index, event)"
            />
          </v-row>
        </v-container>
        <v-container>
          <v-row justify="center">
            <v-btn @click="submitForm" color="red" x-small>Roll</v-btn>
          </v-row>
        </v-container>
      </v-form>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>
