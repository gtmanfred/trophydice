<script setup lang="ts">
import InputNumber from './InputNumber.vue';
</script>
<script lang="ts">
export default {
  props: ["endpoint", "name", "path"],
  mounted() {
    this.client.then((cli) => {
      this.colors = cli.spec.components.schemas.DiceColorEnum.enum;
    });
  },
  computed: {
    colorsLeft: {
      get() {
        return this.colors.filter(
          (color) => !Object.keys(this.diceNums).includes(color)
        );
      },
    },
  },
  methods: {
    changeNumber(color, event) {
      let value = parseInt(event);
      if (isNaN(parseInt(event))) {
        value = parseInt(event.target.value);
        if (isNaN(value)) return;
        this.diceNums[color] = value;
        return;
      }
      this.diceNums[color] = value;
    },
    remove(color) {
      delete this.diceNums[color];
    },
    addColor() {
      if (this.select.color == null) {
        return;
      }
      this.diceNums[this.select.color] = 0;
      this.select.color = null;
    },
    submitForm() {
      this.client.then((client) => {
        client.apis.rolls
          .roll(
            {
              "x-room": this.$route.params.room,
              "x-user-name": window.currentUser
                ? window.currentUser.user
                : "Guest",
            },
            {
              requestBody: { ...this.diceNums },
            }
          )
          .then((response) => {
            console.log(response.obj)
            this.emitter.$emit("roll", response.obj);
            this.$emit("drawer-toggle");
            this.diceNums = {};
          });
      });
    },
  },
  data() {
    return {
      colors: [],
      select: { color: null },
      diceNums: {},
    };
  },
};
</script>

<style scoped>
.select {
  width: 5rem;
}
</style>

<template>
  <v-expansion-panel>
    <v-expansion-panel-title>roll</v-expansion-panel-title>
    <v-expansion-panel-text>
      <v-container v-for="(value, color) in diceNums" v-bind:key="color">
        <v-row justify="center">
          <InputNumber
            :value="value"
            :label="color"
            v-on:input="(event) => changeNumber(color, event)"
          />
        </v-row>
      </v-container>
      <v-container>
        <v-row justify="center">
          <v-select v-model="select.color" :items="colorsLeft" />
          <v-btn @click="addColor" color="red" x-small>add</v-btn>
        </v-row>
      </v-container>
      <v-container>
        <v-row justify="center">
          <v-btn @click="submitForm" color="red" x-small>Roll</v-btn>
        </v-row>
      </v-container>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>
