<template>
  <div class="container-fluid">
    <div class="row">
      <div class="bd-sidebar border-bottom-0 col-md-3 col-xl-4 col-12 border-right" id="sidebar-1" bg-variant="light">
        <!-- Search input -->
        <b-form-input v-model="searchQuery" placeholder="Поиск" class="mt-3 participant-search" />
        <!-- List of search results -->
        <b-list-group class="mt-0  scrollable-sidebar">
          <b-list-group-item v-for="participant in searchedParticipants" :key="participant.id" button
            @click="changeSelectedParticipants(participant.id)" class="participant_items"
            @mousedown="addShadow(participant.id)" :class="{ 'shadowed': participant.shadow }">
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
            <!-- <h4>
              {{ currentParticipantData }}
            </h4> -->
            <div v-if="currentParticipantData">
              <div v-for="(value, key) in currentParticipantData" :key="key">
                <strong>{{ key }}:</strong> {{ value }}
              </div>
            </div>
            <b-button v-b-modal.modal1>Показать заявку</b-button>
            <b-form-select v-model="selectedRank" :options="rankOptions"
              @change="updateRanking(selectedParticipant.id, selectedRank)" class="mt-3"></b-form-select>
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
            <div>
              <b-table striped hover :items="items" :fields="fields"></b-table>
            </div>
          </div>
          <!-- Save button -->
          <b-button type="submit" class="mt-3">Сохранить форму</b-button>
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
  async fetch() {
    //получаем рейтинговую таблицу
    try {
      const event_id = this.$route.query.event_id;
      const nomination_id = this.$route.query.nomination_id;
      const responseC = await axios.get(
        `http://26.134.156.44:8000/events/${event_id}/criteria?nomination_id=${nomination_id}&expert_id=${this.user.id}`,
        {
          headers: {
            Authorization: "Bearer " + this.$cookies.get("token"),
          },
        }
      );
      this.positionCount = responseC.data.position_count;
      this.ratingTable = responseC.data.rating_table;
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
      this.short_info_columns = this.participants[0]['short_info_columns']
    } catch (error) {
      console.error(error);
    }
    // console.log('moun')
    //создаем рейтинговые места

    this.items = Array.from({ length: this.positionCount }, (_, index) => ({
      position: index + 1,
      app_id: null,
    }));

    //настраиваем поля отображения
    // this.fields.push({
    //   key: "short_info_columns",
    //   label: "Короткая информация заявки",
    //   width: "95%",
    //   class: "text-center",
    // });
    this.fields = this.fields.concat(
      this.participants[0].short_info_columns.map(column => ({
        key: column,
        label: column,
        class: 'text-center'
      }))
    );
    //настраиваем опции
    this.rankOptions = [
      { value: null, text: "Выберите место", disabled: true },
      ...Array.from({ length: this.positionCount }, (_, index) => ({
        value: index + 1,
        text: (index + 1).toString(),
      })),
    ];
    //заполняем таблицу
    if (this.ratingTable && this.ratingTable.length > 0) {
      // console.log(this.ratingTable)
      this.ratingTable.forEach((entry) => {
        console.log(entry);
        const item = this.items.find((item) => item.position == entry.position);

        if (item) {
          item.app_id = entry.application_id;
          const participant = this.participants.find(
            (p) => p.id == entry.application_id
          );
          if (participant) {
            // console.log(participant)
            // console.log(participant[participant.short_info_columns[0]])
            // item["short_info_columns"] =
            //   participant[participant.short_info_columns[0]];
            participant.short_info_columns.forEach(column => {
              item[column] = participant[column];
            });
          }
        }
      });
    }
  },
  data() {
    return {
      searchQuery: "",
      participants: [],
      selectedParticipant: {},
      selectedRank: null,
      ratingTable: [],
      positionCount: 0,
      short_info_columns: [],
      fields: [
        {
          key: "position",
          label: "Позиция",
          width: "5%",
          class: "text-center",
        },
      ],
      searchedParticipants: [],
      items: null,
      blank: {
        rating: [],
        eventId: null,
        expertId: null,
        selectedParticipantId: 1,
        //ratingTable: Array.from({ length: 5 }, () => ({ participantId: null })),
        //comments: "",
      },
      rankOptions: [{ value: null, text: "Выберите место", disabled: true }],
    };
  },
  computed: {
    ...mapGetters({
      user: "getUser",
    }),
    // currentParticipantData() {
    //   if (this.selectedParticipant != undefined) {
    //     return this.selectedParticipant[
    //       this.selectedParticipant["short_info_columns"]
    //     ];
    //   }
    // },
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
    }
  },
  watch: {
    searchQuery(newVal) {
      if (newVal === "") {
        this.searchedParticipants = this.participants;
      } else {
        this.searchedParticipants = this.participants.filter((participant) => {
          return participant.short_info_columns.some((key) => {
            return participant[key].toString().toLowerCase().includes(newVal.toLowerCase());
          });
        });
      }
    },
  },

  methods: {
    async changeSelectedParticipants(ParticipantId) {
      this.selectedRank = null;
      this.blank.selectedParticipantId = ParticipantId;
      this.selectedParticipant = this.participants.find(
        (item) => item.id === this.blank.selectedParticipantId
      );
    },

    updateRanking(id, rank) {
      if (this.items[rank - 1]["app_id"] == id) {
        return;
      }
      // this.items.forEach((item) => {
      //   if (item.app_id === id) {
      //     item.app_id = null;
      //     item["short_info_columns"] = null;
      //   }
      // });
      // Обунляем прошлую позицию если участник уже был в таблице
      this.items.forEach((item) => {
        if (item.app_id === id) {
          item.app_id = null;
          this.short_info_columns.forEach((column) => {
            item[column] = null; // Обнуление каждого столбца, указанного в short_info_columns
          });

        }
      });
      // let temp1 = {
      //   app_id: this.items[rank - 1]["app_id"],
      //   short_info_columns: this.items[rank - 1]["short_info_columns"],
      // };
      let temp1 = { ...this.items[rank - 1] };
      delete temp1.position; // удаляем скоированную позицию чтобы не сломать порядок

      const participant = this.participants.find((p) => p.id === id);
      this.$set(this.items[rank - 1], 'app_id', participant.id);
      // this.items[rank - 1]["short_info_columns"] =
      //   participant[participant["short_info_columns"]];
      participant.short_info_columns.forEach(column => {
        this.$set(this.items[rank - 1], column, participant[column]);
      });
      if (temp1.app_id !== null) {
        for (let i = rank; i < this.items.length; i++) {
          // let temp2 = {
          //   app_id: this.items[i]["app_id"],
          //   short_info_columns: this.items[i]["short_info_columns"],
          // };
          let temp2 = { ...this.items[i] };
          delete temp2.position; //также удаляем позицию
          console.log(temp1);
          // this.items[i]["app_id"] = temp1["app_id"];
          // this.items[i]["short_info_columns"] = temp1["short_info_columns"];
          // не работает
          // this.$set(this.items, i, { ...temp1 });
          for (let key in temp1) {
            if (temp1.hasOwnProperty(key)) {
              this.$set(this.items[i], key, temp1[key]);
            }
          }
          console.log(this.items[i]);
          if (!temp2.app_id) {
            return;
          }
          temp1 = temp2;
        }
      }
    },

    async saveEvaluation() {
      try {
        const expertId = this.user.id;
        const eventId = this.$route.query.event_id;
        const nominationId = this.$route.query.nomination_id;
        const filteredCriteria = this.items.filter(
          (item) => item.app_id !== null
        );
        const response = await axios.put(
          `http://26.134.156.44:8000/update_scores`,
          {
            expertId: expertId,
            eventId: eventId,
            nominationId: nominationId,
            criteria: filteredCriteria,
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
    addShadow(participantId) {
      const participant = this.searchedParticipants.find(p => p.id === participantId);
      if (participant) {
        this.$set(participant, 'shadow', true); // Ensure reactivity
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

.participant_items:focus {
  background-color: #d8d8d8 !important
}

.shadowed {
  background-color: #EEEEEE;
  /* Example shadow */
}

.scrollable-sidebar {
  max-height: 81vh;
  /* Высота видимой части экрана */
  overflow-y: auto;
  /* Включает вертикальную прокрутку, если содержимое превышает max-height */
}
</style>
