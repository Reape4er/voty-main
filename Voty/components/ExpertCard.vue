<template>
  <b-card no-body class="d-flex flex-row align-items-center">
    <b-form-checkbox v-model="isChecked" @change="updateExpert"  class="m-2"></b-form-checkbox>
    <div>
      <div>{{ expert.firstname }} {{ expert.surname }} {{ expert.patronymic }}</div>
    </div>
  </b-card>
</template>

<script>
export default {
  props: {
    expert: {
      type: Object,
      required: true
    },
    isSelected: {
      type: Boolean,
      required: true,
      default: false
    }
  },
  data() {
    return {
      isChecked: false
    };
  },
  mounted() {
    this.isChecked = this.isSelected;
  },
  methods:{
    updateExpert(){
      this.$emit("updateExpert", this.isChecked, this.expert)
    }
  }
};
</script>