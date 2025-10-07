<template>
  <div
    class="container d-flex justify-content-center align-items-center vh-100"
  >
    <div class="card p-5">
      <h2 class="mb-4">Регистрация</h2>
      <form @submit.prevent="register">
        <div class="mb-3">
          <label for="firstName" class="form-label">Имя</label>
          <input
            type="text"
            class="form-control"
            id="firstName"
            v-model="User.firstName"
            required
          />
        </div>

        <div class="mb-3">
          <label for="lastName" class="form-label">Фамилия</label>
          <input
            type="text"
            class="form-control"
            id="lastName"
            v-model="User.lastName"
            required
          />
        </div>

        <div class="mb-3">
          <label for="middleName" class="form-label">Отчество</label>
          <input
            type="text"
            class="form-control"
            id="middleName"
            v-model="User.middleName"
            required
          />
        </div>

        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            class="form-control"
            id="email"
            v-model="User.email"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Пароль</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="User.password"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Роль</label>
          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              name="role"
              id="expert"
              value="expert"
              v-model="User.role"
              required
            />
            <label class="form-check-label" for="expert">Эксперт</label>
          </div>
          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              name="role"
              id="organizer"
              value="organizer"
              v-model="User.role"
              required
            />
            <label class="form-check-label" for="organizer">Организатор</label>
          </div>
        </div>

        <button type="submit" class="btn btn-primary">
          Зарегистрироваться
        </button>
      </form>
    </div>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;500;700;900&display=swap"
      rel="stylesheet"
    />
  </div>
</template>

<script>
import axios from "axios";
export default {

  data() {
    return {
      User: {
        firstName: "",
        lastName: "",
        middleName: "",
        email: "",
        password: "",
        role: "",
      },
    };
  },
  methods: {
    async register() {
      console.log(this.User);
      try {
        const response = await axios.post(
          "http://localhost:8000/register",
          this.User
        );
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.container {
  font-family: "Roboto", sans-serif;
}
</style>
