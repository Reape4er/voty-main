<template>
  <div class="container-fluid">
    <div class="row">
      <div class="bd-sidebar border-bottom-0 col-md-3 col-xl-2 col-12 border-right" id="sidebar-1"
        title="Sidebar with Form" bg-variant="light">
        <!-- Search input -->
        <b-form-input v-model="searchQuery" placeholder="Поиск" class="mt-3 participant-search" />
        <!-- List of search results -->
        <b-list-group class="mt-0">
          <b-list-group-item v-for="participant in searchedParticipants" :key="participant.id" button
            @click="changeSelectedParticipants(participant.id)" class="participant_items">
            <!-- {{ participant[participant["short_info_columns"]] }} -->
            <div v-for="column in participant.short_info_columns" :key="column">
              <strong>{{ column }}:</strong> {{ participant[column] }}
            </div>
          </b-list-group-item>
        </b-list-group>
      </div>

      <div class="bd-content col-md-9 col-xl-8 col-12 pb-md-3 pl-md-5">
        <b-form @submit.prevent="saveEvaluation">
          <!-- Отображение имени участника и его проекта-->
          <b-card class="mt-3">
            <h4>
              <!-- {{ currentParticipantData }} -->
              <div v-if="currentParticipantData">
                <div v-for="(value, key) in currentParticipantData" :key="key">
                  <strong>{{ key }}:</strong> {{ value }}
                </div>
              </div>
            </h4>
            <b-button v-b-modal.modal1>Показать заявку</b-button>
          </b-card>

          <!-- Full application details modal -->
          <b-modal id="modal1" title="Детали заявки">
            <div v-for="(value, key) in selectedParticipant" :key="key" v-if="key !== 'id' && key !== 'short_info_columns' && key !== 'status'
          ">
              <strong>{{ key }}</strong> - {{ value }}
            </div>
          </b-modal>

          <!-- Evaluation criteria -->
          <div class="mt-3">
            <b-form-group v-for="item in criterias" :key="item.id">
              <div class="d-flex">
                <h6 class="w-25">{{ item.criteria }}</h6>
                <b-form-select :options="options" v-model="item.value" class="w-auto ml-3" required></b-form-select>
              </div>
            </b-form-group>
          </div>
          <!-- Save button -->
          <b-button type="submit" class="mt-3" variant="success">Сохранить форму</b-button>
        </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  middleware: "auth",

  data() {
    return {
      searchQuery: "",
      participants: [],
      selectedParticipant: {},
      searchedParticipants: [],
      criterias: [],
      blank: {
        eventId: null,
        nominationId: null,
        expertId: null,
        selectedParticipantId: 1,
      },
      options: [
        { text: "Выберите оценку", value: null, disabled: true },
        ...Array.from({ length: 10 }, (_, i) => i + 1),
      ],
    };
  },
  async fetch() {
    //получение критериев
    try {
      const event_id = this.$route.query.event_id;
      const responseC = await axios.get(
        `http://26.134.156.44:8000/events/${event_id}/criteria`,
        {
          headers: {
            Authorization: "Bearer " + this.$cookies.get("token"),
          },
        }
      );
      // Ensure that criteria is always an array
      this.criterias = Array.isArray(responseC.data)
        ? responseC.data.map((criteria) => ({ ...criteria, value: null }))
        : [];
    } catch (error) {
      console.error(error);
    }

    //получение участников
    try {
      const nomination_id = this.$route.query.nomination_id;
      const response = await axios.get(
        `http://26.134.156.44:8000/applications?nomination_id=${nomination_id}&accepted=${true}`,
        {
          headers: {
            Authorization: "Bearer " + this.$cookies.get("token"),
          },
        }
      );
      this.participants = response.data;
      this.searchedParticipants = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  computed: {
    ...mapGetters({
      user: "getUser",
    }),
    currentParticipantData() {
      try {
        if (this.selectedParticipant) {
          let data = {};
          this.selectedParticipant.short_info_columns.forEach(column => {
            data[column] = this.selectedParticipant[column];
          });
          return data;
        }
      } catch (error) {
        console.error("Ошибка при обработке данных участника:", error);
      }
    },
  },
  watch: {
    searchQuery(newVal) {
      if (newVal === "") {
        this.searchedParticipants = this.participants;
      } else {
        this.searchedParticipants = this.participants.filter((participant) => {
          return participant[participant["short_info_columns"]]
            .toLowerCase()
            .includes(newVal.toLowerCase());
        });
      }
    },
  },

  methods: {
    async changeSelectedParticipants(ParticipantId) {
      this.blank.selectedParticipantId = ParticipantId;
      this.selectedParticipant = this.participants.find(
        (item) => item.id === this.blank.selectedParticipantId
      );
      try {
        const nomination_id = this.$route.query.nomination_id;
        this.blank.selectedParticipantId = ParticipantId;
        //запрос на оценку
        const response = await axios.get(
          `http://26.134.156.44:8000/get_score?nomination_id=${nomination_id}&expert_id=${this.user.id}&application_id=${ParticipantId}`,
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        );
        response.data.forEach((score) => {
          const criteriaIndex = this.criterias.findIndex(
            (c) => c.id === score.criteria_id
          );
          if (criteriaIndex !== -1) {
            this.criterias[criteriaIndex].value = score.value;
          }
        });
      } catch (error) {
        this.criterias = this.criterias.map((criteria) => ({
          ...criteria,
          value: null,
        }));
        console.error(error);
      }
    },

    async saveEvaluation() {
      try {
        this.blank.expertId = this.user.id;
        this.blank.eventId = this.$route.query.event_id;
        this.blank.nominationId = this.$route.query.nomination_id;

        const response = await axios.put(
          `http://26.134.156.44:8000/update_scores?eventId=${this.blank.eventId}`,
          {
            ...this.blank,
            criteria: this.criterias,
          },
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        );
        console.log(response.data.message);
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.participant-search {
  margin-bottom: 10px;
  border-color: rgb(84, 192, 192);
  border-radius: 6px;
}

.participant_items {
  margin-top: 5px !important;
  border-radius: 6px;
}
</style>
