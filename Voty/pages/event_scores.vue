<template>
  <div>
    <!-- <button @click="saveToCookies">Сохранить локально</button>
    <button @click="loadFromCookies">Загрузить данные</button>
    <button @click="createProtocol">Составить протокол</button> -->
    <div class="ml-1">
      <b-button @click="updateResult">Сохранить изменения</b-button>
      <b-button @click="createProtocol">Составить протокол</b-button>
    </div>
    <div class="row bg-light border-bottom font-weight-bold text-Medium">
      <!-- <div class="col-1 d-flex align-items-center justify-content-right">
        Переназначить
      </div> -->
      <div class="col-1 d-flex align-items-center justify-content-center">
        Позиция рейтинга
      </div>
      <div class="col-1 d-flex align-items-center justify-content-center">
        Суммарный балл
      </div>
      <div class="col-1 d-flex align-items-center justify-content-center">
        Баллы
      </div>
      <div class="col-1 d-flex align-items-center justify-content-center">
        Дополнительные баллы
      </div>
      <div class="col-5 d-flex align-items-center">
        Короткая информация об участнике
      </div>
      <div class="col-3 d-flex align-items-center">
        Комментарии
      </div>
      <!-- <div class="col-4 d-flex align-items-center">Наименование проекта</div> -->

      <!-- <div class="col-1 d-flex align-items-center justify-content-center">Рекомендации на кубок ректора</div>
      <div class="col-1 d-flex align-items-center justify-content-center">Рекомендация на публикацию в журнале</div>
      <div class="col-1 d-flex align-items-center justify-content-center">Рекомендация на участие в конференции</div> -->
    </div>
    <draggable v-model="eventScores" @end="updateRanks" :options="{ handle: '.handle' }">
      <div class="row bg-light border-bottom text-large" v-for="(item, index) in eventScores" :key="item.id">
        <!-- <div class="handle col-1 d-flex align-items-center justify-content-center">
          ::
        </div> -->
        <div class="col-1 d-flex align-items-center justify-content-center">
          {{ index + 1 }}
        </div>
        <div class="col-1 d-flex align-items-center justify-content-center">
          <strong>{{ item.total_result }}</strong>
        </div>
        <div class="col-1 d-flex align-items-center justify-content-center">
          {{ item.result }}
        </div>
        <div class="col-1 d-flex align-items-center justify-content-center">
          <b-form-spinbutton vertical size="sm" v-model="item.additional_score" min="0"
            @change="updateTable"></b-form-spinbutton>
        </div>
        <!-- <div class="col-9 d-flex align-items-center">
          {{ getParticipantInfo(item.application_id) }}
        </div> -->
        <div class="col-5 d-flex flex-column align-items-left">
          <div v-for="(value, key) in getParticipantInfo(item.application_id)" :key="key">
            <strong>{{ key }}</strong>: {{ value }}
          </div>
        </div>
        <div class="col-3 d-flex flex-column align-items-left">
          <b-form-textarea v-model=item.comments />
        </div>
        <!-- <div class="col-4 d-flex align-items-center">{{ item.report_title }}</div> -->

        <!-- <div class="col-1 d-flex align-items-center justify-content-center">
          <input type="radio" :value="item.id" v-model="cupNominee" />
        </div>
        <div class="col-1 d-flex align-items-center justify-content-center">
          <input type="checkbox" :value="item.id" v-model="journalPublications" />
        </div>
        <div class="col-1 d-flex align-items-center justify-content-center">
          <input type="checkbox" :value="item.id" v-model="conferenceParticipations" />
        </div> -->
      </div>
    </draggable>
  </div>
</template>

<script>
import axios from "axios";
import draggable from "vuedraggable";
import { saveAs } from "file-saver";

export default {
  components: {
    draggable,
  },
  data() {
    return {
      eventScores: [], // Здесь будут данные с бэка
      cupNominee: null,
      journalPublications: [],
      conferenceParticipations: [],
      participants: [],
    };
  },
  async fetch() {
    try {
      const nomination_id = this.$route.query.nomination_id;
      const response = await axios.get(
        `http://26.134.156.44:8000/result?nomination_id=${nomination_id}`,
        {
          headers: {
            Authorization: "Bearer " + this.$cookies.get("token"),
          },
        }
      );
      response.data.forEach(item => {
        if (item.additional_score === null) {
          item.additional_score = 0;
        }
        item.total_result = item.result + item.additional_score;
      });
      console.log(response.data);

      this.eventScores = response.data.sort((a, b) => b.total_result - a.total_result);

      // Присваиваем ранг каждому элементу
      this.eventScores.forEach((score, index) => {
        score.rank = index + 1;
      });
    } catch (error) {
      console.error("Error fetching event scores:", error);
      this.eventScores = [];
    }
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
      // this.searchedParticipants = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    updateRanks() {
      // Обновляем ранги всех элементов
      this.eventScores.forEach((score, index) => {
        score.rank = index + 1;
      });
    },
    updateTable() {
      this.eventScores.forEach(item => {
        item.total_result = item.result + item.additional_score;
      });
      this.eventScores.sort((a, b) => b.total_result - a.total_result);
      this.updateRanks();
    },
    // getParticipantInfo(itemId) {
    //   const participant = this.participants.find(
    //     (participant) => participant.id === itemId
    //   );
    //   console.log(participant);
    //   return participant
    //     ? participant[participant["short_info_columns"]]
    //     : "No info available";
    // },
    async updateResult() {
      try {
        const nomination_id = this.$route.query.nomination_id;
        const response = await axios.put(
          `http://26.134.156.44:8000/result?nomination_id=${nomination_id}`,
          this.eventScores,
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        );
        // this.searchedParticipants = response.data;
      } catch (error) {
        console.error(error);
      }
    },

    getParticipantInfo(itemId) {
      const participant = this.participants.find(p => p.id === itemId);
      if (participant) {
        let info = {};
        participant.short_info_columns.forEach(column => {
          info[column] = participant[column];
        });
        return info;
      } else {
        return { error: "No info available" };
      }
    },
    saveToCookies() {
      localStorage.setItem("eventScores", JSON.stringify(this.eventScores));
      this.$cookies.set("eventScores", this.eventScores);
      this.$cookies.set("cupNominee", this.cupNominee);
      this.$cookies.set("journalPublications", this.journalPublications);
      this.$cookies.set(
        "conferenceParticipations",
        this.conferenceParticipations
      );
    },
    loadFromCookies() {
      this.eventScores = JSON.parse(localStorage.getItem("eventScores"));
      this.cupNominee = this.$cookies.get("cupNominee") || null;
      this.journalPublications = this.$cookies.get("journalPublications") || [];
      this.conferenceParticipations =
        this.$cookies.get("conferenceParticipations") || [];
    },
    createProtocol() {
      const nomination_id = this.$route.query.nomination_id;


      this.$axios
        .get(`http://26.134.156.44:8000/get_protocol?nomination_id=${nomination_id}`, {
          responseType: "arraybuffer",
        })
        .then((response) => {
          console.log(response.headers);
          const contentType =
            response.headers["content-type"] || "application/octet-stream";
          const blob = new Blob([response.data], { type: contentType });
          saveAs(blob, "filename.docx");
        })
        .catch((error) => {
          console.error("Error creating protocol:", error);
        });
    },
  },

  /*watch: {
    eventScores: {
      handler() {
        this.saveToCookies();
      },
      deep: true,
    },
    cupNominee() {
      this.saveToCookies();
    },
    journalPublications: {
      handler() {
        this.saveToCookies();
      },
      deep: true,
    },
    conferenceParticipations: {
      handler() {
        this.saveToCookies();
      },
      deep: true,
    },
  },*/
};
</script>

<style scoped>
.handle {
  cursor: move;
}

.text-large {
  font-size: 1.1rem;
  padding: 10px;
}
</style>
