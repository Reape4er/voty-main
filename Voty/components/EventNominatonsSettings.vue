<template>
  <div>
    <!-- Add nomination button -->
    <b-button
      variant="primary"
      class="mb-3"
      block
      @click="createNomination"
      :disabled="isCreateDisabled"
    >
      Добавить номинацию
    </b-button>
    <nomination-card
      v-for="nomination in nominations"
      :key="nomination.id"
      :nominationId="nomination.id"
      :nominationName="nomination.nomination_name"
      :selectedExperts="nomination.users"
      @OpenExpertsModal="OpenExpertsModal"
      @updateNomination="updateNomination"
      @nominationNameChanged="nominationNameChanged"
      @deleteNomination="deleteNomination"
    />
    <ExpertsModal
      :selectedExperts="selectedExperts"
      :nominationId="modalNominationId"
      @updateSelectedExperts="updateSelectedExperts"
      ref="expertsModal"
    />
  </div>
</template>

<script>
import NominationCard from "~/components/NominationCard.vue";
import axios from "axios";
export default {
  components: {
    NominationCard,
  },
  data() {
    return {
      isCreateDisabled: false,
      nominations: [],
      eventId: null,
      selectedExperts: [],
      modalNominationId: -1,
    };
  },
  async fetch() {
    // Вызывайте функцию для получения мероприятий после создания компонента
    // this.getContests();
    try {
      const eventId = this.$route.query.id;
      const response = await axios.get(
        `http://localhost:8000/events/${eventId}/nominations`,
        {
          headers: {
            Authorization: "Bearer " + this.$cookies.get("token"),
          },
        }
      );
      this.nominations = response.data;
      //console.log(response);
      //console.log(this.contests);
    } catch (error) {
      console.error("Error fetching contests:", error);
    }
  },
  methods: {
    async createNomination() {
      try {
        const eventId = this.$route.query.id;
        this.isCreateDisabled = true;
        const response = await axios.post(
          `http://localhost:8000/events/${eventId}/nominations`,
          {},
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        );
        this.nominations.push(response.data);
        this.isCreateDisabled = false;
      } catch (error) {
        console.error(error);
        this.isCreateDisabled = false;
      }
    },
    async updateNomination(nominationId) {
      const nomination = this.nominations.find(
        (nomination) => nomination.id === nominationId
      );
      if (!nomination) {
        console.error("Nomination not found with id:", nominationId);
      }
      try {
        const eventId = this.$route.query.id;
        const nomination = this.nominations.find(
          (nomination) => nomination.id === nominationId
        );
        const response = await axios.put(
          `http://localhost:8000/events/${eventId}/nominations/${nomination.id}`,
          nomination,
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        );
      } catch (error) {
        console.error("Error:", error);
      }
    },
    OpenExpertsModal(selectedExperts, nominationId) {
      this.selectedExperts = selectedExperts;
      this.modalNominationId = nominationId;
      this.$refs.expertsModal.openModal();
    },
    updateSelectedExperts(selectedExperts, nominationId) {
      const index = this.nominations.findIndex(
        (nomination) => nomination.id === nominationId
      );
      if (index !== -1) {
        this.$set(this.nominations[index], "users", selectedExperts);
      } else {
        console.error("Nomination not found with id:", nominationId);
      }
    },
    nominationNameChanged(newNominationName, nominationId) {
      const index = this.nominations.findIndex(
        (nomination) => nomination.id === nominationId
      );
      if (index !== -1) {
        this.$set(
          this.nominations[index],
          "nomination_name",
          newNominationName
        );
      } else {
        console.error("Nomination not found with id:", nominationId);
      }
    },
    async deleteNomination(nominationId) {
      const eventId = this.$route.query.id;
      try {
        // Send the delete request to the backend
        await axios.delete(
          `http://localhost:8000/events/${eventId}/nominations/${nominationId}`,
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        );
        // If the request is successful, find the index of the nomination to be deleted
        const index = this.nominations.findIndex(
          (nomination) => nomination.id === nominationId
        );
        if (index !== -1) {
          // Remove the nomination from the array
          this.nominations.splice(index, 1);
        } else {
          console.error("Nomination not found with id:", nominationId);
        }
      } catch (error) {
        console.error("Error deleting nomination:", error);
      }
    },
  },
};
</script>
