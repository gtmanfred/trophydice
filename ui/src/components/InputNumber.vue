<template>
  <v-text-field :label="label" :outline="outline"  :model-value="value">
    <template v-slot:prepend>
      <v-btn @click.stop="decrease()" class="changer">-</v-btn>
    </template>
    <template v-slot:append>
      <v-btn @click.stop="increase()" color="grey--darken-2">+</v-btn>
    </template>
  </v-text-field>
</template>

<script lang="ts">
export default {
  name: "VInputNumber",
  props: {
    label: {
      type: String,
      default: "",
    },

    min: {
      type: Number,
      default: 0,
    },

    max: {
      type: Number,
      default: 9999,
    },

    maxLength: {
      type: Number,
      default: 4,
    },

    outline: {
      type: Boolean,
      default: true,
    },

    step: {
      type: Number,
      default: 1,
    },

    value: [String, Number],
  },

  computed: {
    mask() {
      let mask = "";
      for (let i = 0; i < this.maxLength; i++) mask = `${mask}#`;
      return mask;
    },
  },

  methods: {
    increase() {
      if (isNaN(parseInt(this.value))) return this.$emit("input", this.step);
      if (this.value === this.max) return;
      this.$emit("input", parseInt(this.value) + this.step);
    },

    decrease() {
      if (isNaN(parseInt(this.value))) return this.$emit("input", this.min);
      if (this.value === this.min) return;
      this.$emit("input", parseInt(this.value) - this.step);
    },
  },
};
</script>
