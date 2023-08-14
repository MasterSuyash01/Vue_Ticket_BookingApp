<template>
  <div class="container mt-5">
    <h1 class="text-center">Login</h1>
    <form @submit.prevent="loginUser" class="w-50 mx-auto mt-5">
      <!-- Username field -->
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input
          type="text"
          v-model="username"
          class="form-control"
          id="username"
          required
        />
      </div>
      <!-- Password field -->
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          v-model="password"
          class="form-control"
          id="password"
          required
        />
      </div>
      <!-- Login button -->
      <button type="submit" class="btn btn-primary">Login</button>
      <p v-if="error" class="text-danger mt-3">{{ error }}</p>
    </form>
    <!-- New User Registration Button -->
    <div class="text-center mt-4">
      <router-link class="btn btn-success" to="/user/registration">
        Register New User
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      error: "",
    };
  },
  methods: {
    loginUser() {
      const loginData = {
        username: this.username,
        password: this.password,
      };

      axios
        .post("http://127.0.0.1:5000/login", loginData)
        .then((response) => {
          if (response.status == 200) {
            // set token in local storage
            localStorage.setItem("access_token", response.data.access_token);
            if (response.data.is_admin) {
              this.$router.push("/admin/dashboard");
            } else {
              this.$router.push("/user/dashboard");
            }
          } else {
            this.error = "An error occurred. Please try again.";
          }
        })
        .catch((error) => {
          this.error =
            error.response.data.message ||
            "An error occurred. Please try again.";
          console.error(error);
        });
    },
  },
  created() {
    // check if user is already logged in
    if (localStorage.getItem("access_token")) {
      // fetch check_login
      axios
        .get("http://127.0.0.1:5000/check_login", {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
        })
        .then((response) => {
          if (response.status == 200) {
            if (response.data.is_admin) {
              this.$router.push("/admin/dashboard");
            } else {
              this.$router.push("/user/dashboard");
            }
          }
        })
        .catch((error) => {
          localStorage.removeItem("access_token");
          console.error(error);
        });
    } else {
      localStorage.removeItem("access_token");
    }
  },
};
</script>
