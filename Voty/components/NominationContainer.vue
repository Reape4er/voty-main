<template>
  <!--для отображения блоков существующих номинаций на странице номинаций конкретного мероприятия-->
  <b-card>
    <h2 class="contest-title">{{ nominationData.nomination_name }}</h2>
    <div class="contest-description">
      Статус мероприятия: {{ nominationStatus }}
    </div>
    <div>
      <div class="contest-description">Назначенные эксперты:</div>
      <div
        v-for="expert in nominationData.users"
        :key="expert.id"
        class="contest-description ml-3"
      >
        {{ expert.firstname + " " + expert.surname + " " + expert.patronymic }}
      </div>
    </div>
    <div v-if="user.role === 'organizer'">
      <div class="mt-1" style="display: flex; justify-content: flex-start">
        <a
          class="contest-manage_edit_button"
          @click="$emit('startNomination', nominationData)"
          >Запустить номинацию</a
        >
        <nuxt-link
          :to="`/applications?nomination_id=${nominationData.id}`"
          class="contest-manage_edit_button ml-3"
          >Управление анкетами</nuxt-link
        >
        <a
          class="contest-manage_edit_button ml-3"
          @click="$emit('CalculateResult', nominationData.id)"
          >Подсчет итогов</a
        >
        <nuxt-link
          :to="`/event_scores?nomination_id=${nominationData.id}`"
          class="contest-manage_edit_button ml-3"
          >Просмотр итоговой таблицы</nuxt-link
        >
      </div>
    </div>
    <div v-else>
      <div class="mt-1" style="display: flex; justify-content: flex-start">
        <a
          @click.prevent="connectToNomination"
          class="contest-manage_edit_button"
          >Подключиться на оценивание</a
        >
      </div>
    </div>
  </b-card>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
export default {
  props: {
    nominationData: {
      type: Object,
      required: true,
    },
  },
  computed: {
    nominationStatus() {
      return this.nominationData.nomination_status == 1
        ? "запущено"
        : "не запущено";
    },
    ...mapGetters({
      user: "getUser",
    }),
  },
  methods: {
    connectToNomination() {
      if (this.nominationData.nomination_status == 0) {
        return;
      }
      if (!this.nominationData.users) {
        return;
      }
      if (!this.nominationData.users.some((user) => user.id === this.user.id)) {
        console.error("Current user is not part of the nomination users");
        return;
      }
      axios
        .get(
          `http://localhost:8000/events/${this.nominationData.event_id}`,
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        )
        .then((response) => {
          console.log("Event data:", response.data);
          console.log("Event data:", this.nominationData.id);
          if (response.data["evaluation_method"] == 0) {
            this.$router.push(
              `/evaluation?event_id=${this.nominationData.event_id}&nomination_id=${this.nominationData.id}`
            );
          } else if (response.data["evaluation_method"] == 1) {
            this.$router.push(
              `/ratingEvaluation?event_id=${this.nominationData.event_id}&nomination_id=${this.nominationData.id}`
            );
          }
          // Handle the response data as needed
        })
        .catch((error) => {
          console.error("Error fetching event data:", error);
          // Handle errors as needed
        });
    },
  },
};
</script>

<style scoped>
.contest-title {
  margin-bottom: 10px;
  font-size: 24px;
  font-weight: 700;
  color: #464646;
}
.contest-description,
.contest-experts,
.contest-period {
  font-size: 15px;
  font-weight: 300;
  color: #474747;
}
.contest-evaluation-method {
  color: #616161;
}
.contest-manage_edit_button {
  cursor: pointer;
  text-decoration: none;
}
.contest-manage_delete_button {
  color: #be6363;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.1s ease;
  margin-left: auto;
  margin-right: 15px;
}
</style>
