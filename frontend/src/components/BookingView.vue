<template>
  <div class="booking-form">
    <h1 class="text-center">Booking Form</h1>
    <form @submit.prevent="submitBooking" class="w-50 mx-auto mt-5">
      <!-- Name field -->
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

      <!-- Show name field -->
      <div class="mb-3">
        <label for="showName" class="form-label">Show Name</label>
        <select
          type="text"
          v-model="showName"
          class="form-control"
          id="showName"
          @change="showSelect"
          required
        >
          <option value="" disabled>Select a show</option>
          <option v-for="show in shows" :key="show.id" :value="show.id">
            {{ show.title }}
          </option>
        </select>
        <p v-show="venue" class="mt-2 p-2 border">
          Venue: {{ venue.theatre }}, {{ venue.place }}, {{ venue.city }}
        </p>
      </div>

      <!-- Date field -->
      <div class="mb-3">
        <label for="date" class="form-label">Date</label>
        <input
          type="Date"
          v-model="date"
          class="form-control"
          id="date"
          required
          disabled
        />
      </div>
      <!-- Time field -->
      <div class="mb-3">
        <label for="time" class="form-label">Time</label>
        <input
          type="time"
          v-model="time"
          class="form-control"
          id="time"
          required
          disabled
        />
      </div>
      <!-- Number of tickets field -->
      <div class="mb-3">
        <label for="numTickets" class="form-label">Number of Tickets</label>
        <input
          type="number"
          v-model="numTickets"
          class="form-control"
          id="numTickets"
          required
        />
      </div>

      <!-- Submit button -->
      <button type="submit" class="btn btn-primary">Book Tickets</button>
    </form>
  </div>
</template>
<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "",
      date: "",
      time: "",
      numTickets: 1,
      showName: "",
      shows: [],
      venue: "",
      selectedShow: "",
      token: "", // Populate this array with show data
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
  methods: {
    showSelect() {
      this.selectedShow = this.shows.find((show) => show.id == this.showName);
      this.venue = this.selectedShow.venue;
      this.date = this.selectedShow.date;
      this.time = this.selectedShow.time;
    },
    submitBooking() {
      const bookingData = {
        name: this.name,
        date: this.date,
        time: this.time,
        num_tickets: this.numTickets,
        showname: this.showName,
      };

      axios
        .post("http://127.0.0.1:5000/bookings", bookingData, this.axiosConfig)
        .then((response) => {
          if (response.status == 201) {
            alert("Booking successful!");
            this.$router.push("/user/dashboard");
          }
        })
        .catch((error) => {
          alert("Error booking tickets : " + error.response.data.message);
          this.$router.push("/user/dashboard");
        });
    },
    fetchShows() {
      axios
        .get("http://127.0.0.1:5000/shows", this.axiosConfig)
        .then((response) => {
          this.shows = response.data.shows;
        })
        .catch((error) => {
          console.error("Error fetching shows:", error);
        });
    },
  },
  mounted() {
    let token = localStorage.getItem("access_token");
    if (token == null) {
      this.$router.push("/login");
    } else {
      this.token = token;
    }
    this.fetchShows();
  },
};
</script>

<style>
/* Add your custom styles here */
.booking-form {
  padding: 20px;
}
</style>
