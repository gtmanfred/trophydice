<template>
  <v-row justify="center">
    <v-card>
      <v-divider />
      <v-card-text v-html="message"></v-card-text>
      <v-card-text>
        <img
          v-for="die in dice"
          v-bind:key="die.uuid"
          :src="die.link"
          :class="dieStyle(die)"
        />
      </v-card-text>
    </v-card>
  </v-row>
</template>

<script start>
export default {
  props: ["message", "dice"],
  methods: {
    dieStyle(die) {
      if (die.highest === false) {
        return "lower";
      }
      return "";
    },
  },
};
</script>

<style scoped>
div:deep(strong) {
  font-weight: bold;
}

.lower {
  height: 70px;
  width: auto;
}
</style>
