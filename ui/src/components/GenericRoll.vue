<script lang="ts">
export default {
  props: ["endpoint", "name", "path"],
  mounted() {
    this.client.then((cli) => {
      this.colors = cli.spec.components.schemas.DiceColorEnum.enum;
    });
  },
  computed: {
    room: {
      get() {
        return window.location.href.split("#").pop();
      },
    },
    colorsLeft: {
      get() {
        return this.colors.filter(
          (color) => !Object.keys(this.diceNums).includes(color)
        );
      },
    },
  },
  methods: {
    increment(color) {
      this.diceNums[color]++;
    },
    decrement(color) {
      if (this.diceNums[color] == 0) {
        return;
      }
      this.diceNums[color]--;
    },
    remove(color) {
      delete this.diceNums[color];
    },
    addColor() {
      if (this.selectedColor == null) {
        return;
      }
      this.diceNums[this.selectedColor] = 0;
      this.selectedColor = null;
    },
    submitForm() {
      const config = {
        headers: {
          "x-room": this.room,
          "x-user-name": window.currentUser ? window.currentUser.user : "Guest",
          "content-type": "application/json",
        },
      };
      this.axios
        .post(`${window.location.origin}/api/v2/roll`, this.diceNums, config)
        .then(() => {
          this.$emit("drawer-toggle");
          this.diceNums = {};
        });
    },
  },
  data() {
    return {
      colors: [],
      selectedColor: null,
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
          <v-chip>{{ color }} {{ value }}</v-chip>
          <v-btn @click="decrement(color)" class="changer">-</v-btn>
          <v-btn @click="increment(color)" color="grey--darken-2">+</v-btn>
        </v-row>
      </v-container>
      <v-container>
        <v-row justify="center">
          <v-select v-model="selectedColor" :items="colorsLeft"></v-select>
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
