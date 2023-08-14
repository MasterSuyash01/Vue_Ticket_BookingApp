<template>
  <div class="container mt-5">
    <h1 class="text-center">User Registration</h1>
    <form @submit.prevent="registerUser" class="w-50 mx-auto mt-5">
      <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input
          type="text"
          v-model="name"
          class="form-control"
          id="name"
          required
        />
      </div>
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
      <div class="mb-3">
        <label for="confirmPassword" class="form-label">Confirm Password</label>
        <input
          type="password"
          v-model="confirmPassword"
          class="form-control"
          id="confirmPassword"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
      <p v-if="error" class="text-danger mt-3">{{ error }}</p>
    </form>

    <!-- Back to User Login Button -->
    <div class="text-center mt-4">
      <button class="btn btn-secondary" @click="goToUserLogin">
        Back to User Login
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "",
      username: "",
      password: "",
      confirmPassword: "",
      error: "",
    };
  },
  methods: {
    registerUser() {
      if (this.password !== this.confirmPassword) {
        this.error = "Passwords do not match.";
        return;
      }

      // Make a POST request to the backend for user registration
      const registrationData = {
        name: this.name,
        username: this.username,
        password: this.password,
        confirmPassword: this.confirmPassword,
      };

      axios
        .post("http://127.0.0.1:5000/register", registrationData)
        .then(() => {
          this.error = "";
          // Registration successful, redirect to the user login page
          if (this.$route.name !== "UserLogin") {
            // Check if the current route is not already "UserLogin" to avoid redundant navigation
            this.$router.push({ name: "UserLogin" });
          }
        })
        .catch((error) => {
          this.error = "Registration failed. Please try again.";
          console.error(error);
        });
    },
    goToUserLogin() {
      // Redirect back to the user login page.
      this.$router.push({ name: "UserLogin" });
    },
  },
};
</script>
