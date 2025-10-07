<template>
  <b-card>
    <b-row class="flex align-items-center">
      <!-- Левая часть с знаком "+" -->
      <div class="m-1" style="width: 3%;">
        <b-button @click="toggleList">
        <span class="plus" v-if="isListVisible">-</span>
        <span class="plus" v-else>+</span>
        </b-button>
      </div>

      <!-- Правая часть с полем ввода и кнопкой -->
      <div class="m-1" style="width: 95%;">

        <b-form-group>
          <b-form-input
            v-model.lazy="localNominationName"
            placeholder="Введите название номинации"
            v-if="isListVisible"
          >
          </b-form-input>
          <h6 v-else>{{ localNominationName }}</h6>
        </b-form-group>

        <transition name="list-expand" mode="out-in">
          <div v-if="isListVisible">
            <b-button @click="$emit('OpenExpertsModal',selectedExperts, nominationId)" variant="success">Изменить список экспертов</b-button>
            <!-- Список экспертов -->
            <b-list-group class="mt-3">
              <b-list-group-item v-for="expert in selectedExperts" :key="expert.id">
                {{ expert.firstname +" "+ expert.surname +" "+ expert.patronymic }}
              </b-list-group-item>
            </b-list-group>
            <div class="mt-3 d-flex justify-content-between">
              <b-button 
                @click="$emit('updateNomination', nominationId)"
                variant="primary"
              >Сохранить</b-button>
              <b-button 
                @click="$emit('deleteNomination', nominationId)"
                variant="danger"
              >Удалить</b-button>
            </div>
          </div>
        </transition>

      </div>
    </b-row>
  </b-card>
  
</template>

<script>
export default {
  props: {
    nominationId: {
      type: Number,
      required:true
    },
    nominationName: {
      type: String,
      required: true
    },
    selectedExperts: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  data() {
    return {
      isListVisible: false,
      isCardClicked: true, // Track if the card is clicked
      isEditable: false,
      localNominationName: this.nominationName,
    };
  },
  methods: {
    toggleList() {
      this.isListVisible = !this.isListVisible;
    }
  },
  watch: {
  localNominationName(newVal) {
    this.$emit('nominationNameChanged', newVal, this.nominationId);
  }
}
}
</script>

<style scoped>
.list-expand-enter-active, .list-expand-leave-active {
  transition: all 0.5s ease;
}
.list-expand-enter, .list-expand-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}
.plus {
  width: 20px;
}
/* Hover effect */
.hover-effect:hover {
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Example shadow */
  background-color: #ecf9ff; /* Slightly blue background color */
}

/* Active (click) effect */
.card-active {
  box-shadow: 0 8px 16px rgba(0,0,0,0.2); /* More pronounced shadow */
}

/* Transition effect for the list */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>