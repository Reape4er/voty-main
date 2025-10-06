<template>
  <div>
    <b-table :items="applications" :fields="fields" striped responsive="sm">
      <template #cell(show_details)="row">
        <b-button size="sm" @click="row.toggleDetails" class="mr-2">
          {{ row.detailsShowing ? "Скрыть" : "Показать" }} детали
        </b-button>

        <!-- As `row.showDetails` is one-way, we call the toggleDetails function on @change -->
        <!-- <b-form-checkbox v-model="row.detailsShowing" @change="row.toggleDetails">
            Details via check
          </b-form-checkbox> -->
      </template>

      <template #row-details="row">
        <b-card>
          <!-- Define the fields you want to exclude -->
          <b-row
            class="mb-2"
            v-for="(value, key) in row.item"
            :key="key"
            v-if="!['short_info_columns', '_showDetails'].includes(key)"
          >
            <b-col sm="3" class="text-sm-right"
              ><b>{{ key }}:</b></b-col
            >
            <b-col>{{ value }}</b-col>
          </b-row>
          <b-button size="sm" @click="row.toggleDetails"
            >Скрыть детали</b-button
          >
          <b-button
            variant="success"
            size="sm"
            @click="acceptApplication(row.item.id, row)"
            >Принять заявку</b-button
          >
          <b-button
            variant="danger"
            size="sm"
            @click="rejectApplication(row.item.id, row)"
            >Отклонить заявку</b-button
          >
        </b-card>
      </template>
    </b-table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  middleware: "auth",
  data() {
    return {
      applications: null,
      fields: null,
    };
  },
  async fetch() {
    try {
      const nominationId = this.$route.query.nomination_id;
      const response = await axios.get(
        `http://26.134.156.44:8000/applications?nomination_id=${nominationId}`,
        {
          headers: {
            Authorization: "Bearer " + this.$cookies.get("token"),
          },
        }
      );
      // this.applications = response.data;
      this.applications = response.data.map((application) => {
        return {
          ...application,
          status: application.status ? "Принята" : "Не принята",
        };
      });
      //ключ с содержанием колонок для отображения
      this.fields = this.applications[0]["short_info_columns"];
      //колонка для отображения деталей
      this.fields.push("show_details");
      //ключ для статуса заявки с бека
      this.fields.push("status");
      console.log(this.fields);

      //console.log(response);
      console.log(this.applications);
    } catch (error) {
      console.error("Error fetching contests:", error);
    }
  },
  methods: {
    async acceptApplication(applicationId, row) {
      await axios
        .put(
          `http://26.134.156.44:8000/applications?application_id=${applicationId}`,
          {
            application_status: true,
          },
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        )
        .then((response) => {
          // Обновите локальный статус заявки
          const application = this.applications.find(
            (app) => app.id === applicationId
          );
          if (application) {
            application.status = "Принята";
            row.toggleDetails();
          }
        })
        .catch((error) => {
          console.error("Error accepting application:", error);
        });
    },
    async rejectApplication(applicationId, row) {
      await axios
        .put(
          `http://26.134.156.44:8000/applications?application_id=${applicationId}`,
          {
            application_status: false,
          },
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        )
        .then((response) => {
          // Обновите локальный статус заявки
          const application = this.applications.find(
            (app) => app.id === applicationId
          );
          if (application) {
            application.status = "Не принята";
            row.toggleDetails();
          }
        })
        .catch((error) => {
          console.error("Error accepting application:", error);
        });
    },
  },
};
</script>
