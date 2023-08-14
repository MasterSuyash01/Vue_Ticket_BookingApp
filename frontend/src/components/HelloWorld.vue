<template>
  <div class="landing-page">
    <header class="header">
      <h1 class="title">Ticket Show Booking</h1>
      <p class="subtitle">Book your favorite shows now!</p>
    </header>

    <main class="main">
      <section class="show-list">
        <h2 class="section-title">Upcoming Shows</h2>
        <ul>
          <li v-for="show in upcomingShows" :key="show.id" class="show-item">
            <div class="show-details">
              <h3 class="show-title">{{ show.title }}</h3>
              <p class="show-genre">{{ show.genre }}</p>
              <p class="show-date-time">{{ show.date }} at {{ show.time }}</p>
            </div>
            <button class="book-now-btn" @click="redirectToUserLogin">
              Book Now
            </button>
          </li>
        </ul>
      </section>
    </main>

    <footer class="footer">
      <p>&copy; 2023 Ticket Show Booking App</p>
    </footer>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      upcomingShows: [],
    };
  },
  methods: {
    redirectToUserLogin() {
      this.$router.push({ name: "UserLogin" });
    },
    fetchUpcomingShows() {
      const path = "http://127.0.0.1:5000/shows"; // Replace with your API endpoint
      axios
        .get(path)
        .then((res) => {
          this.upcomingShows = res.data.shows; // Assuming the API response structure is similar
        })
        .catch((error) => {
          console.error("Error fetching upcoming shows:", error);
        });
    },
  },

  created() {
    this.fetchUpcomingShows();
  },
};
</script>

<style>
/* Add your custom styles here */
.landing-page {
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.title {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 18px;
}

.main {
  max-width: 800px;
  margin: 0 auto;
}

.section-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.show-list {
  margin-bottom: 30px;
}

.show-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
}

.show-details {
  flex: 1;
}

.show-title {
  font-size: 20px;
  font-weight: bold;
}

.show-genre {
  font-size: 16px;
}

.show-date-time {
  font-size: 16px;
  margin-top: 5px;
}

.book-now-btn {
  font-size: 16px;
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.book-now-btn:hover {
  background-color: #0056b3;
}

.footer {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #777;
}
</style>
