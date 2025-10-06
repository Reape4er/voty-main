<template>
  <div class="main-block">
    <div class="contests-header">
      <h1 class="page-title">МЕРОПРИЯТИЯ</h1>
      <div v-if="user.role === 'organizer'">
        <b-button
          variant="outline-primary"
          @click="createEvent"
          :disabled="isCreateDisabled"
          >Добавить новое мероприятие</b-button
        >
      </div>
    </div>
    <div>
      <div>
        <div
          class="contests-container"
          v-for="contest in contests"
          :key="contest.id"
        >
          <EventContainer
            class="contest-block"
            :eventData="contest"
            @deleteEvent="deleteContest"
          />
        </div>
      </div>
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
      <link
        href="https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;500;700;900&display=swap"
        rel="stylesheet"
      />
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";
import EventContainer from "../components/EventContainer.vue";

export default {
  data() {
    return {
      contests: [],
      isCreateDisabled: false,
    };
  },
  middleware: "auth",
  computed: {
    ...mapGetters({
      user: "getUser",
    }),
  },
  async fetch() {
    // Вызывайте функцию для получения мероприятий после создания компонента
    try {
      const response = await axios.get("http://26.134.156.44:8000/events", {
        headers: {
          Authorization: "Bearer " + this.$cookies.get("token"),
        },
      });
      this.contests = response.data;
      //console.log(response);
      //console.log(this.contests);
    } catch (error) {
      console.error("Error fetching contests:", error);
    }
  },

  methods: {
    async createEvent() {
      try {
        this.isCreateDisabled = true;
        const response = await axios.post(
          "http://26.134.156.44:8000/events",
          {},
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        );
        this.$router.push({
          path: "/settings",
          query: { id: response.data.id },
        });
      } catch (error) {
        console.error(error);
        this.isCreateDisabled = false;
      }
    },

    async deleteContest(contest) {
      try {
        const response = await axios.delete(
          `http://26.134.156.44:8000/events/${contest.id}`,
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        );

        if (response.status === 200) {
          // await this.getContests();
          this.contests = this.contests.filter((c) => c.id !== contest.id);
        }
      } catch (error) {
        console.error("Error deleting contest:", error);
      }
    },

    async connectToContest(contestId, evaluationMethod) {
      try {
        const response = await axios.get(
          `http://26.134.156.44:8000/check_status?eventId=${contestId}&id=${this.user.id}`,
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        );
        if (evaluationMethod == "arifmetic") {
          console.log(evaluationMethod);
          this.$router.push(`/evaluation?eventId=${contestId}`);
        } else {
          this.$router.push(`/ratingEvaluation?eventId=${contestId}`);
        }
      } catch (error) {
        console.error(error.response);
      }
    },
  },
};
</script>

<style scoped>
.contests-header {
  width: 80%;
  margin: auto;
  padding-left: 20px;
}
.page-title {
  margin-top: 40px;
  font-size: 24px;
  font-weight: 700;
  text-align: center;
  color: #474747da;
}

.contests-container {
  width: 80%;
  margin: auto;
  padding: 10px;
  font-family: "Roboto", sans-serif;
}

.contest-block {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  transition: transform 0.3s ease;
}

.contest-block:hover {
  background-color: #e4ecf0b0;
  border-color: rgba(189, 206, 218, 0.719);
  transform: scale(1.01);
}

.contest-manage_add_new_contest {
  cursor: pointer;
  text-decoration: none;
  font-size: 17px;
  font-weight: 700;
}

.contest-manage_buttons {
  display: flex;
  justify-content: flex-start;
  margin: 0 auto;
  font-size: 15px;
  font-weight: 500;
}

.contest-manage_start_button {
  color: #616161;
  cursor: pointer;
  text-decoration: none;
}

.contest-manage_view_results_button {
  color: #79968c;
  cursor: pointer;
  text-decoration: none;
  margin-left: 100px;
}

.contest-manage_delete_button:hover {
  color: #f5745e;
}
</style>
