<template>
  <v-card class="card">
    <div v-html="message"></div>
    <img
      v-for="die in dice"
      v-bind:key="die.uuid"
      :src="die.link"
      :class="dieStyle(die)"
    />
  </v-card>
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

.details {
  flex: 1;
  margin-left: 1rem;
}

.card {
  display: block;
  margin: auto;
}

.lower {
  height: 70px;
  width: auto;
}

img.card {
  display: float;
}

@media() {
  .item {
    margin-top: 0;
    padding: 0.4rem 0 1rem calc(var(--section-gap) / 2);
  }

  .item:before {
    content: " ";
    border-left: 1px solid var(--color-border);
    position: absolute;
    left: 0;
    bottom: calc(50% + 25px);
    height: calc(50% - 25px);
  }

  .item:after {
    content: " ";
    border-left: 1px solid var(--color-border);
    position: absolute;
    left: 0;
    top: calc(50% + 25px);
    height: calc(50% - 25px);
  }

  .item:first-of-type:before {
    display: none;
  }

  .item:last-of-type:after {
    display: none;
  }
}
</style>
