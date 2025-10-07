<template>
  <div>
    <div class="main-block">
      <h1 class="page-title">НОМИНАЦИИ</h1>
      <div
        class="contests-container"
        v-for="nomination in nominations"
        :key="nomination.id"
      >
        <NominationContainer
          class="contest-block"
          :nominationData="nomination"
          @startNomination="startNomination"
          @CalculateResult="CalculateResult"
        />
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
import axios from "axios";
import NominationContainer from "../components/NominationContainer.vue";
export default {
  middleware: "auth",
  data() {
    return {
      nominations: null,
    };
  },
  async fetch() {
    try {
      const eventId = this.$route.query.eventid;
      const response = await axios.get(
        `http://26.134.156.44:8000/events/${eventId}/nominations`,
        {
          headers: {
            Authorization: "Bearer " + this.$cookies.get("token"),
          },
        }
      );
      this.nominations = response.data;
      console.log(this.nominations);
    } catch (error) {
      console.error("Error fetching contests:", error);
    }
  },

  methods: {
    async startNomination(nomination) {
      if (!nomination) {
        console.error("Nomination not found");
        return;
      }
      //eventid не важен
      const eventId = 0;
      const nominationCopy = { ...nomination };
      nominationCopy["nomination_status"] =
        !nominationCopy["nomination_status"];
      axios
        .put(
          `http://26.134.156.44:8000/events/${eventId}/nominations/${nominationCopy.id}`,
          nominationCopy,
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        )
        .then((response) => {
          if (response.status == 204) {
            const index = this.nominations.findIndex(
              (n) => n.id === nominationCopy.id
            );
            if (index !== -1) {
              this.$set(this.nominations, index, {
                ...this.nominations[index],
                ...nominationCopy,
              });
            }
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
    async CalculateResult(nominationId) {
      try {
        const result = await axios.post(
          `http://26.134.156.44:8000/result`,
          { nomination_id: nominationId },
          {
            headers: {
              Authorization: "Bearer " + this.$cookies.get("token"),
            },
          }
        );
        console.log(result); // Optionally handle the result
      } catch (error) {
        console.error("Error calculating result:", error);
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
