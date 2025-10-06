<template>
  <b-modal size="lg" v-model="showModal" title="Список экспертов">
    <div v-for="expert in allExperts" :key="expert.id" class="mb-2">
      <ExpertCard
        :expert="expert"
        :isSelected="isExpertSelected(expert)"
        @updateExpert="updateExpert"
      />
    </div>
    <template #modal-footer>
      <b-button variant="secondary" @click="showModal = false"
        >Закрыть</b-button
      >
    </template>
  </b-modal>
</template>

<script>
//   import ExpertRow from './ExpertRow.vue';
import axios from "axios";
export default {
  // components: {
  //   ExpertRow
  // },
  props: {
    selectedExperts: {
      type: Array,
      required: true,
    },
    nominationId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      showModal: false,
      allExperts: [],
      newSelectedExperts: [],
    };
  },
  // beforeUpdate() {
  //   this.newSelectedExperts = [...this.selectedExperts];
  //   console.log("абоба",this.newSelectedExperts)
  // },
  watch: {
    selectedExperts: {
      deep: true,
      handler(newVal) {
        this.newSelectedExperts = [...newVal];
        console.log("вотчер");
      },
    },
  },
  async fetch() {
    try {
      const response = await axios.get(
        `http://26.134.156.44:8000/users/experts`,
        {
          headers: {
            Authorization: "Bearer " + this.$cookies.get("token"),
          },
        }
      );
      this.allExperts = response.data;
    } catch (error) {
      console.error("Error fetching contests:", error);
    }
  },
  methods: {
    openModal() {
      this.showModal = true;
    },
    isExpertSelected(expert) {
      return this.newSelectedExperts.some(
        (selectedExpert) => selectedExpert.id === expert.id
      );
    },
    updateExpert(flag, expert) {
      const index = this.newSelectedExperts.findIndex(
        (e) => e.id === expert.id
      );
      if (flag) {
        // Если флаг true и эксперт не найден в массиве, добавляем его
        if (index === -1) {
          this.newSelectedExperts.push(expert);
          this.$emit(
            "updateSelectedExperts",
            this.newSelectedExperts,
            this.nominationId
          );
          console.log("Добавлен эксперт");
        }
      } else {
        // Если флаг false и эксперт найден, удаляем его из массива
        if (index !== -1) {
          this.newSelectedExperts.splice(index, 1);
          this.$emit(
            "updateSelectedExperts",
            this.newSelectedExperts,
            this.nominationId
          );
          console.log("Удален эксперт");
        }
      }
    },
  },
};
</script>
