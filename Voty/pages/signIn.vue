<template>
  <div
    class="container d-flex justify-content-center align-items-center vh-100"
  >
    <div class="card p-5">
      <h2 class="text-center mb-5">Вход</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="User.email"
            class="form-control"
            required
          />
        </div>
        <div class="form-group mt-3">
          <label for="password">Пароль</label>
          <input
            type="password"
            id="password"
            v-model="User.password"
            class="form-control"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary mt-4">Войти</button>
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
import axios from 'axios';
export default {
  data() {
    return {
      User:{   
      email: "",
      password: ""}
  
    };
  },
  methods: {
    async submitForm() {
      console.log(this.User)
      try {
        const response = await axios.post('http://26.134.156.44:8000/login', this.User);
        console.log(response.data);
        this.$cookies.set('token', response.data.access_token);
        console.log(this.$cookies.get('token'))
        this.$router.push('/')
      } catch (error) {
        console.error(error);
      }
    }
  },
};
</script>

<style scoped>
.container {
  font-family: "Roboto", sans-serif;
  height: 100vh;
}
</style>
