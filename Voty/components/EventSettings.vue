<template>
  <div class="main_div">
    <b-container fluid>
      <h1>Настройки мероприятия</h1>
      <b-form @submit.prevent="onSubmit">
        <!-- Название мероприятия -->
        <b-form-group label="Название мероприятия">
          <b-form-input v-model="eventTitle" required></b-form-input>
        </b-form-group>
        <!-- Описание мероприятия -->
        <b-form-group label="Описание мероприятия">
          <b-form-textarea v-model="eventDescription" rows="3" max-rows="6"></b-form-textarea>
        </b-form-group>
        <!-- Указание статуса мероприятия-->
        <b-form-group label="Укажите статус мероприятия">
          <b-form-select required v-model="eventLevel" :options="statusOptions"></b-form-select>
        </b-form-group>
        <!-- Указание столбца для парсинга номинаций -->
        <b-form-group
          label="Укажите столбец из excel файла участников, которые будут использоваться для создания номинаций">
          <b-form-input v-model="nominationsColumn"></b-form-input>
        </b-form-group>
        <!-- Указание столбца для отметки об отображении -->
        <b-form-group
          label="Укажите название столбца для краткого отображения данных об анкете из excel файла анкет участников">
          <div v-for="(column, index) in toShowColumn" :key="index" class="mt-1">
            <b-form-input v-model="toShowColumn[index]"></b-form-input>
          </div>
          <b-button @click="addColumn" class="mt-2">Добавить столбец</b-button>
        </b-form-group>

        <!-- Загрузка файла участников -->
        <b-form-group label="Загрузка excel файла участников">
          <b-form-file v-model="participantsFile" accept=".xls,.xlsx"></b-form-file>
        </b-form-group>
        <div>Будут созданы номинации: {{ nomination_list }}</div>
        <b-button @click="uploadApplications">Создать номинации и добавить участников</b-button>

        <!-- Метод оценивания -->
        <b-form-group label="Метод оценивания">
          <b-form-radio-group v-model="evaluationMethod">
            <b-form-radio :value="0">Среднее арифметическое</b-form-radio>
            <b-form-radio :value="1">Рейтинговая</b-form-radio>
          </b-form-radio-group>
        </b-form-group>

        <!-- Вопросы для мероприятий -->
        <b-form-group v-if="evaluationMethod === 0" label="Критерии мероприятия">
          <div v-for="(question, index) in questions" :key="index" class="question mt-1">
            <span class="question-number">{{ index + 1 }}.</span>
            <b-form-input v-model="questions[index].criteria" required></b-form-input>
          </div>
          <b-button class="mt-2" @click="addQuestion" variant="primary">Добавить вопрос</b-button>
        </b-form-group>
        <b-form-spinbutton v-else v-model="rankingNumber" min="0"></b-form-spinbutton>
        <b-button class="mt-2" type="submit" variant="primary">Сохранить</b-button>
      </b-form>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import * as XLSX from "xlsx";

export default {
  data() {
    return {
      eventTitle: "",
      eventDescription: "",
      eventLevel: null,
      nominationsColumn: "",
      toShowColumn: [],
      foundColumns: [],
      nomination_list: [null],
      participantsFile: null,
      participants: [],
      evaluationMethod: 0,
      nominations: [],
      questions: [],
      rankingNumber: 0,
      statusOptions: [
        { value: null, text: "Выберите статус", disabled: true },
        { value: 0, text: "Университетское" },
        { value: 1, text: "Региональное" },
        { value: 2, text: "Межрегиональное" },
        { value: 3, text: "Всероссийское" },
        { value: 4, text: "Международное" },
      ],
      // key: [],
    };
  },
  async fetch() {
    const eventId = this.$route.query.id;
    const response = await this.$axios.$get(
      "http://localhost:8000/events/" + eventId,
      {
        headers: {
          Authorization: "Bearer " + this.$cookies.get("token"),
        },
      }
    );
    console.log(response);
    this.eventTitle = response.event_name;
    this.eventDescription = response.event_description;
    this.evaluationMethod = response.evaluation_method;
    this.eventLevel = response.event_level;
    this.questions = response.arithmetics_parameters || [];
    this.rankingNumber = response.ratings_parameters || 0;
  },
  methods: {
    onSubmit() {
      // Получаем id из параметра запроса
      const eventId = this.$route.query.id;

      if (eventId) {
        // Если eventId существует, отправляем запрос на обновление
        axios
          .put(
            `http://localhost:8000/events/${eventId}`,
            {
              event_name: this.eventTitle,
              event_description: this.eventDescription,
              evaluation_method: this.evaluationMethod,
              event_level: this.eventLevel,
              arithmetics_parameters: this.questions,
              ratings_parameters: this.rankingNumber,
            },
            {
              headers: {
                Authorization: "Bearer " + this.$cookies.get("token"),
              },
            }
          )
          .catch((error) => {
            console.error("Error updating event:", error);
          });
      }
    },

    addQuestion() {
      const eventId = this.$route.query.id;
      this.questions.push({
        event_id: eventId,
        criteria: "",
        criteria_weight: 1,
      });
    },
    uploadApplications() {
      const eventId = this.$route.query.id;
      if (
        this.nomination_list.length === 1 &&
        (this.nomination_list[0] === null ||
          this.nomination_list[0] === undefined)
      ) {
        // Здесь можно выбросить ошибку или обработать ситуацию по-другому
        console.error("Ошибка: список номинаций не может быть пустым.");
        return;
      }
      if (this.toShowColumn === "" || this.toShowColumn === null) {
        console.error("Ошибка: отсуствует столбец для отображения.");

        return;
      }
      axios
        .post(
          `http://localhost:8000/applications/upload`,
          {
            event_id: eventId,
            applications: this.participants,
            nomination_column: this.nominationsColumn,
            to_show_column: this.foundColumns,
          },
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        )
        .catch((error) => {
          console.error("Error updating event:", error);
        });
    },
    addColumn() {
      this.toShowColumn.push('');
    },
    // addQuestion(){
    //   // запрос на создание критерия
    // },
  },
  watch: {
    participantsFile(newFile) {
      try {
        const reader = new FileReader();
        reader.onload = (e) => {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: "array" });
          const worksheet = workbook.Sheets[workbook.SheetNames[0]];
          const jsonData = XLSX.utils.sheet_to_json(worksheet);
          const headers = Object.keys(jsonData[0]);
          this.foundColumns = headers.filter(header => this.toShowColumn.includes(header));
          console.log(jsonData)
          this.nomination_list = [
            ...new Set(jsonData.map((item) => item[this.nominationsColumn])),
          ];
          if (
            this.nomination_list.length === 1 &&
            (this.nomination_list[0] === null ||
              this.nomination_list[0] === undefined)
          ) {
            // Здесь можно выбросить ошибку или обработать ситуацию по-другому
            console.error("Ошибка: список номинаций не может быть пустым.");
            return;
          }
          console.log(this.nomination_list);
          // Заполнение списка всех участников, если список номинаций не пуст
          this.participants = jsonData;

          console.log(this.participants);
        };
        reader.readAsArrayBuffer(newFile);
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
