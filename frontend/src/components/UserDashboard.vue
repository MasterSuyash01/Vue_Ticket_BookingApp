<template>
  <div class="user-dashboard">
    <h1 class="text-center">Welcome to the User Dashboard</h1>
    <div>
      <button type="button" class="btn btn-outline-light">
        <router-link to="/user/login">Back to User Login</router-link>
      </button>
      <button type="button" class="btn btn-outline-light">
        <router-link to="/user/booking">Book Tickets</router-link>
      </button>
      <!-- Button to export theateres -->
      <button type="button" @click="export_th" class="btn btn-primary">
        Export Theatres
      </button>
    </div>
    <b-form @submit="onSearch" class="mb-3">
      <b-form-group label="Search by Show Title:" label-for="search-input">
        <b-input-group>
          <b-form-input
            id="search-input"
            v-model="searchKeyword"
            placeholder="Enter show title..."
          ></b-form-input>
          <b-input-group-append>
            <b-button type="submit" variant="outline-secondary"
              >Search</b-button
            >
          </b-input-group-append>
        </b-input-group>
      </b-form-group>
    </b-form>

    <div class="container mt-5">
      <h2>Your Bookings</h2>
      <div v-for="booking in bookings" :key="booking.id" class="booking-item">
        <p><strong>Show:</strong> {{ booking.showname }}</p>
        <p><strong>Venue:</strong> {{ booking.venuename }}</p>
        <p><strong>Date:</strong> {{ booking.date }}</p>
        <p><strong>Time:</strong> {{ booking.time }}</p>
        <p><strong>Number of Tickets:</strong> {{ booking.num_tickets }}</p>
      </div>
    </div>
    <div class="container mt-5">
      <h2>All Shows</h2>
      <div v-for="show in shows" :key="show.id" class="booking-item">
        <p><strong>Show:</strong> {{ show.title }}</p>
        <p>
          <strong>Venue:</strong> {{ show.venue.theatre }}
          {{ show.venue.place }}
        </p>
        <p><strong>Date:</strong> {{ show.date }}</p>
        <p><strong>Time:</strong> {{ show.time }}</p>
        <p><strong>Number of Tickets:</strong> {{ show.num_tickets }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      bookings: [],
      shows: [],
      searchKeyword: "",
      token: "",
      originalShows: [],
    };
  },
  computed: {
    axiosConfig() {
      return {
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
      };
    },
  },

  created() {
    // Fetch user's bookings and all shows when the component is created
    let token = localStorage.getItem("access_token");
    if (token == null) {
      this.$router.push("/login");
    } else {
      this.token = token;
    }
    this.fetchBookings();
    this.fetchShows();
    // Store the original list of shows
  },

  methods: {
    export_th() {
      axios
        .get("http://127.0.0.1:5000/export/theatres", this.axiosConfig) // Adjust the URL accordingly
        .then((response) => {
          // get the blob make anchor tag and click to download theatres.csv
          const blob = new Blob([response.data], { type: "text/csv" });
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = url;
          link.download = "theatres.csv";
          link.click();
        });
    },
    fetchBookings() {
      // Make a GET request to fetch user's bookings
      axios
        .get("http://127.0.0.1:5000/bookings", this.axiosConfig) // Adjust the URL accordingly
        .then((response) => {
          this.bookings = response.data.bookings;
        })
        .catch((error) => {
          console.error("Error fetching bookings:", error);
        });
    },
    fetchShows() {
      // Make a GET request to fetch all shows
      axios
        .get("http://127.0.0.1:5000/shows", this.axiosConfig) // Adjust the URL accordingly
        .then((response) => {
          this.shows = response.data.shows;
          this.originalShows = [...this.shows];
        })
        .catch((error) => {
          alert("Error fetching shows : " + error);
        });
    },
    onSearch(e) {
      e.preventDefault();
      if (this.searchKeyword.trim() === "") {
        this.shows = [...this.originalShows];
      } else {
        this.shows = this.originalShows.filter((show) =>
          show.title
            .toLowerCase()
            .includes(this.searchKeyword.trim().toLowerCase())
        );
      }
      this.searchKeyword = ""; // Reset the search input after searching
    },
  },
};
</script>

<style>
/* Add your custom styles here */
.user-dashboard {
  padding: 20px;
}
.booking-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
</style>
