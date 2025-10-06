<template>
  <div class="row">
    <div class="col-xs-12 col-sm-3 col-md-3 col-lg-2 border-right p-0" >
      <b-button-group vertical class="full-width">
        <b-button
        :class="{'active': currentComponent === 'EventSettings'}"
        squared
        variant="primary"
        @click="currentComponent = 'EventSettings'"
        >
        Настройки мероприятий
        </b-button>
        <b-button
        :class="{'active': currentComponent === 'EventNominatonsSettings'}"
        squared
        variant="primary"
        @click="currentComponent = 'EventNominatonsSettings'"
        >
        Настройка номинаций
      </b-button>
      </b-button-group>
    </div>

    <div class="col-xs-12 col-sm-8 col-md-9 col-lg-10">
      <KeepAlive>
        <component :is="currentComponent"></component>
      </KeepAlive>
    </div>
  </div>
</template>
<script>
import EventSettings from '@/components/EventSettings.vue';
import EventNominatonsSettings from '@/components/EventNominatonsSettings.vue';
export default {
  middleware: "auth",
  data() {
    return {
      currentComponent: 'EventSettings',
    };
  },
  components: {
    EventSettings,
    EventNominatonsSettings,
  },
};
</script>
<style scoped>
.full-width {
  width: 100%;
}
</style>