<template>
  <div>
    <header>
      <b-navbar>
        <b-navbar-nav>
          <nuxt-link to="/">
            <img src="VOTY.png" alt="Logo" class="navbar-logo" />
          </nuxt-link>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto mr-3">
          <b-dropdown v-if="!!this.user" :text="fullName" class="navigation_button">
            <b-dropdown-item v-if="this.user.role === 'organizer'"><nuxt-link
                to="/register">Зарегистрировать</nuxt-link></b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item @click="logout">Выход</b-dropdown-item>
          </b-dropdown>
        </b-navbar-nav>
      </b-navbar>
    </header>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;500;700;900&display=swap"
      rel="stylesheet" />
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters({
      user: "getUser",
    }),
    fullName() {
      if (this.user) {
        return `${this.user.lastName} ${this.user.firstName} ${this.user.middleName}`;
      }
      return "";
    },
  },
  methods: {
    logout() {
      this.$cookies.remove("token");
      this.$router.push("/signin");
      this.$store.commit("REMOVE_USER");
    },
  },
};
</script>

<style scoped>
header {
  background-color: #ffffff;
  padding: 1em;
}

.navbar-logo {
  max-height: 25px;
  width: auto;
  opacity: 0.7;
}

.navigation_button {
  color: rgb(20, 33, 39);
  font-family: "Roboto", sans-serif;
  font-size: 17px;
  font-weight: 300;
}
</style>
