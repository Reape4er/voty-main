<template>
    <b-alert
      :show="show"
      :variant="variant"
      dismissible
      @dismissed="show = false"
      style="position: fixed; top: 20px; right: 20px; z-index: 2000;"
    >
      {{ message }}
    </b-alert>
  </template>
  
  <script>
  export default {
    props: {
      variant: {
        type: String,
        default: 'info' // 'success', 'danger', 'warning'
      },
      message: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        show: false
      };
    },
    methods: {
      display() {
        this.show = true;
        setTimeout(() => {
          this.show = false;
        }, 3000);
      }
    },
    mounted() {
      this.display();
    }
  }
  </script>