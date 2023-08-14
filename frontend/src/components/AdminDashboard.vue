<template>
  <div class="container">
    <h1 class="text-center bg-primary text-white" style="border-radius: 10px">
      Ticket Show Booking Admin 🎫
    </h1>
    <hr />
    <br />

    <!-- Alert -->
    <b-alert variant="success" v-if="showMessage" show>
      {{ message }}
    </b-alert>
    <div>
      <!-- Add Show button -->
      <button
        type="button"
        class="btn btn-success btn-md"
        @click="showAddShowModal()"
      >
        Add Show
      </button>

      <button
        type="button"
        class="btn btn-success btn-"
        @click="showAddVenueModal()"
      >
        Add Venue
      </button>
    </div>
    <br /><br />
    <button @click="logout" class="btn btn-danger">Logout</button>

    <!-- Search Form -->
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

    <!-- Shows Table -->
    <table class="table table-hover">
      <thead>
        <tr>
          <th scope="col">Title</th>
          <th scope="col">Venue</th>
          <th scope="col">Genre</th>
          <th scope="col">Date</th>
          <th scope="col">Time</th>
          <th scope="col">Number of Tickets</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(show, index) in shows" :key="index">
          <td>{{ show.title }}</td>
          <td>{{ show.venue.theatre }} {{ show.venue.place }}</td>
          <td>{{ show.genre }}</td>
          <td>{{ show.date }}</td>
          <td>{{ show.time }}</td>
          <td>{{ show.num_tickets }}</td>
          <td>
            <div class="btn-group" role="group">
              <button
                type="button"
                class="btn btn-info btn-sm"
                @click="showEditModal(show)"
              >
                Update
              </button>
              <button
                type="button"
                class="btn btn-danger btn-sm"
                @click="deleteShow(show)"
              >
                Delete
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Venues Table -->
    <table class="table table-hover">
      <thead>
        <tr>
          <th scope="col">Theatre</th>
          <th scope="col">Place</th>
          <th scope="col">City</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(venue, index) in venues" :key="index">
          <td>{{ venue.theatre }}</td>
          <td>{{ venue.place }}</td>
          <td>{{ venue.city }}</td>
          <td>
            <div class="btn-group" role="group">
              <button
                type="button"
                class="btn btn-info btn-sm"
                @click="venueEditModal(venue)"
              >
                Update
              </button>
              <button
                type="button"
                class="btn btn-danger btn-sm"
                @click="deleteVenue(venue)"
              >
                Delete
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Add Show Modal -->
    <b-modal
      ref="addShowModal"
      id="show-modal"
      title="Add a new show"
      hide-backdrop
      hide-footer
    >
      <!-- Add Show Form -->
      <b-form @submit="onShowSubmit" @reset="onReset" class="w-100">
        <b-form-group
          id="form-title-group"
          label="Title:"
          label-for="form-title-input"
        >
          <b-form-input
            id="form-title-input"
            type="text"
            v-model="addShowForm.title"
            required
            placeholder="Enter show title"
          />
        </b-form-group>
        <!-- Add a drop down to select venue -->
        <b-form-group
          id="form-venue-group"
          label="Venue:"
          label-for="form-venue-input"
        >
          <b-form-select
            id="form-venue-input"
            v-model="addShowForm.venue"
            required
            placeholder="Select venue"
          >
            <option v-for="venue in venues" :key="venue.id" :value="venue.id">
              {{ venue.theatre }} {{ venue.place }} {{ venue.city }}
            </option>
          </b-form-select>
        </b-form-group>

        <b-form-group
          id="form-genre-group"
          label="Genre:"
          label-for="form-genre-input"
        >
          <b-form-input
            id="form-genre-input"
            type="text"
            v-model="addShowForm.genre"
            required
            placeholder="Enter show genre"
          />
        </b-form-group>

        <b-form-group
          id="form-date-group"
          label="Date:"
          label-for="form-date-input"
        >
          <b-form-input
            id="form-date-input"
            type="date"
            v-model="addShowForm.date"
            required
          />
        </b-form-group>

        <b-form-group
          id="form-time-group"
          label="Time:"
          label-for="form-time-input"
        >
          <b-form-input
            id="form-time-input"
            type="time"
            v-model="addShowForm.time"
            required
          />
        </b-form-group>
        <b-form-group>
          <b-form-input
            id="form-tickets-input"
            type="number"
            v-model="addShowForm.num_tickets"
            required
            placeholder="Enter number of tickets"
          />
        </b-form-group>

        <b-button type="submit" variant="outline-info">Submit</b-button>
        <b-button type="reset" variant="outline-danger">Reset</b-button>
      </b-form>
    </b-modal>

    <!-- Edit Show Modal -->
    <b-modal
      ref="editShowModal"
      id="show-update-modal"
      title="Update Show"
      hide-backdrop
      hide-footer
    >
      <!-- Edit Show Form -->
      <b-form @submit="onUpdateShow" @reset="onResetUpdate" class="w-100">
        <b-form-group
          id="form-title-edit-group"
          label="Title:"
          label-for="form-title-edit-input"
        >
          <b-form-input
            id="form-title-edit-input"
            type="text"
            v-model="editShowForm.title"
            required
            placeholder="Enter show title"
          />
        </b-form-group>

        <b-form-group
          id="form-venue-edit-group"
          label="Venue:"
          label-for="form-venue-edit-input"
        >
          <b-form-select
            id="form-venue-edit-input"
            v-model="editShowForm.venue"
            required
            placeholder="Select venue"
          >
            <option v-for="venue in venues" :key="venue.id" :value="venue.id">
              {{ venue.theatre }}
            </option>
          </b-form-select>
        </b-form-group>

        <b-form-group
          id="form-genre-edit-group"
          label="Genre:"
          label-for="form-genre-edit-input"
        >
          <b-form-input
            id="form-genre-edit-input"
            type="text"
            v-model="editShowForm.genre"
            required
            placeholder="Enter show genre"
          />
        </b-form-group>

        <b-form-group
          id="form-date-edit-group"
          label="Date:"
          label-for="form-date-edit-input"
        >
          <b-form-input
            id="form-date-edit-input"
            type="date"
            v-model="editShowForm.date"
            required
          />
        </b-form-group>

        <b-form-group
          id="form-time-edit-group"
          label="Time:"
          label-for="form-time-edit-input"
        >
          <b-form-input
            id="form-time-edit-input"
            type="time"
            v-model="editShowForm.time"
            required
          />
        </b-form-group>
        <b-form-group>
          <b-form-input
            id="form-tickets-edit-input"
            type="number"
            v-model="editShowForm.num_tickets"
            required
            placeholder="Enter number of tickets"
          />
        </b-form-group>

        <b-button-group>
          <b-button type="submit" variant="outline-info">Update</b-button>
          <b-button type="reset" variant="outline-danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <!-- Add Venue Modal -->
    <b-modal
      ref="addVenueModal"
      id="venue-modal"
      title="Add a new venue"
      hide-backdrop
      hide-footer
    >
      <!-- Add Venue Form -->
      <b-form @submit="onVenueSubmit" @reset="onReset" class="w-100">
        <b-form-group
          id="form-theatre-group"
          label="Theatre:"
          label-for="form-theatre-input"
        >
          <b-form-input
            id="form-theatre-input"
            type="text"
            v-model="addVenueForm.theatre"
            required
            placeholder="Enter theatre name"
          />
        </b-form-group>

        <b-form-group
          id="form-place-group"
          label="Place:"
          label-for="form-place-input"
        >
          <b-form-input
            id="form-place-input"
            type="text"
            v-model="addVenueForm.place"
            required
            placeholder="Enter place"
          />
        </b-form-group>

        <b-form-group
          id="form-city-group"
          label="City:"
          label-for="form-city-input"
        >
          <b-form-input
            id="form-city-input"
            type="text"
            v-model="addVenueForm.city"
            required
            placeholder="Enter city"
          />
        </b-form-group>

        <b-button type="submit" variant="outline-info">Submit</b-button>
        <b-button type="reset" variant="outline-danger">Reset</b-button>
      </b-form>
    </b-modal>

    <!-- Edit Venue Modal -->
    <b-modal
      ref="editVenueModal"
      id="venue-update-modal"
      title="Update Venue"
      hide-backdrop
      hide-footer
    >
      <!-- Edit Venue Form -->
      <b-form @submit="onUpdateVenue" @reset="onResetUpdate" class="w-100">
        <b-form-group
          id="form-theatre-edit-group"
          label="Theatre:"
          label-for="form-theatre-edit-input"
        >
          <b-form-input
            id="form-theatre-edit-input"
            type="text"
            v-model="editVenueForm.theatre"
            required
            placeholder="Enter theatre name"
          />
        </b-form-group>

        <b-form-group
          id="form-place-edit-group"
          label="Place:"
          label-for="form-place-edit-input"
        >
          <b-form-input
            id="form-place-edit-input"
            type="text"
            v-model="editVenueForm.place"
            required
            placeholder="Enter place"
          />
        </b-form-group>

        <b-form-group
          id="form-city-edit-group"
          label="City:"
          label-for="form-city-edit-input"
        >
          <b-form-input
            id="form-city-edit-input"
            type="text"
            v-model="editVenueForm.city"
            required
            placeholder="Enter city"
          />
        </b-form-group>

        <b-button-group>
          <b-button type="submit" variant="outline-info">Update</b-button>
          <b-button type="reset" variant="outline-danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <!-- Footer -->
    <footer
      class="bg-primary text-white text-center"
      style="border-radius: 10px"
    >
      Copyright &copy; All Rights Reserved {{ new Date().getFullYear() }}.
    </footer>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TicketShowBookingAdmin",

  data() {
    return {
      shows: [],
      venues: [],
      addShowForm: {
        title: "",
        genre: "",
        date: "",
        time: "",
        venue: "",
        num_tickets: "",
      },
      addVenueForm: {
        theatre: "",
        place: "",
        city: "",
      },
      editShowForm: {
        id: "",
        title: "",
        genre: "",
        date: "",
        time: "",
        venue: "",
        num_tickets: "",
      },
      editVenueForm: {
        id: "",
        theatre: "",
        place: "",
        city: "",
      },
      showMessage: false,
      message: "",
      searchKeyword: "",
      token: "",
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
    getShows() {
      const path = "http://127.0.0.1:5000/shows";
      axios
        .get(path, this.axiosConfig)
        .then((res) => {
          this.shows = res.data.shows;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getVenues() {
      const path = "http://127.0.0.1:5000/venues";
      axios
        .get(path, this.axiosConfig)
        .then((res) => {
          this.venues = res.data.venues;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    showAddShowModal() {
      this.$refs.addShowModal.show();
    },
    showAddVenueModal() {
      this.$refs.addVenueModal.show();
    },
    addShow(payload) {
      const path = "http://127.0.0.1:5000/shows"; // Replace with your API endpoint
      axios
        .post(path, payload, this.axiosConfig)
        .then((response) => {
          if (response.data.status === "success") {
            // Show added successfully, update the shows list
            this.shows.push(response.data.show);
            this.message = "Show Added 🎉!";
            this.showMessage = true;
          } else {
            console.error("Failed to add show:", response.data.message);
          }
        })
        .catch((error) => {
          console.error("Error adding show:", error);
        });
    },
    addVenue(payload) {
      const path = "http://127.0.0.1:5000/venues"; // Replace with your API endpoint
      axios
        .post(path, payload, this.axiosConfig)
        .then((response) => {
          if (response.data.status === "success") {
            // Show added successfully, update the shows list
            this.venues.push(response.data.venue);
            this.message = "Venue Added 🎉!";
            this.showMessage = true;
          } else {
            console.error("Failed to add venue:", response.data.message);
          }
        })
        .catch((error) => {
          console.error("Error adding venue:", error);
        });
    },

    showEditModal(show) {
      this.editShowForm = { ...show };
      this.$refs.editShowModal.show();
    },

    venueEditModal(venue) {
      this.editVenueForm = { ...venue };
      this.$refs.editVenueModal.show();
    },

    onShowSubmit(e) {
      e.preventDefault();
      this.$refs.addShowModal.hide();
      const payload = {
        title: this.addShowForm.title,
        genre: this.addShowForm.genre,
        date: this.addShowForm.date,
        time: this.addShowForm.time,
        venue: this.addShowForm.venue,
        num_tickets: this.addShowForm.num_tickets,
      };
      this.addShow(payload);
      this.initShowForm();
    },

    onVenueSubmit(e) {
      e.preventDefault();
      this.$refs.addVenueModal.hide();
      const payload = {
        theatre: this.addVenueForm.theatre,
        place: this.addVenueForm.place,
        city: this.addVenueForm.city,
      };
      this.addVenue(payload);
      this.initVenueForm();
    },

    onUpdateShow(e) {
      e.preventDefault();
      this.$refs.editShowModal.hide();
      const payload = {
        title: this.editShowForm.title,
        genre: this.editShowForm.genre,
        date: this.editShowForm.date,
        time: this.editShowForm.time,
        venue: this.editShowForm.venue,
        num_tickets: this.editShowForm.num_tickets,
      };
      this.updateShow(payload, this.editShowForm.id);
    },

    updateShow(payload, showID) {
      const path = `http://127.0.0.1:5000/shows/${showID}`;
      axios
        .put(path, payload, this.axiosConfig)
        .then(() => {
          // Remove the old show from the list and add the updated one
          this.shows = this.shows.map((show) =>
            show.id === showID ? { ...show, ...payload } : show
          );

          this.message = "Show updated ⚙️!";
          this.showMessage = true;
          this.$refs.editShowModal.hide();
        })
        .catch((error) => {
          console.error(error);
        });
    },

    onUpdateVenue(e) {
      e.preventDefault();
      this.$refs.editVenueModal.hide();
      const payload = {
        theatre: this.editVenueForm.theatre,
        place: this.editVenueForm.place,
        city: this.editVenueForm.city,
      };
      this.updateVenue(payload, this.editVenueForm.id);
    },

    updateVenue(payload, venueID) {
      const path = `http://127.0.0.1:5000/venues/${venueID}`;
      axios
        .put(path, payload, this.axiosConfig)
        .then(() => {
          // Remove the old show from the list and add the updated one
          this.venues = this.venues.map((venue) =>
            venue.id === venueID ? { ...venue, ...payload } : venue
          );

          this.message = "Venue updated ⚙️!";
          this.showMessage = true;
          this.$refs.editVenueModal.hide();
        })
        .catch((error) => {
          console.error(error);
        });
    },

    deleteVenue(venue) {
      const path = `http://127.0.0.1:5000/venues/${venue.id}`;
      axios
        .delete(path, this.axiosConfig)
        .then(() => {
          this.shows = this.shows.filter((s) => s.id !== venue.id);
          this.message = "Venue Removed 🗑️!";
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deleteShow(show) {
      const path = `http://127.0.0.1:5000/shows/${show.id}`;
      axios
        .delete(path, this.axiosConfig)
        .then(() => {
          this.shows = this.shows.filter((s) => s.id !== show.id);
          this.message = "Show Removed 🗑️!";
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    logout() {
      // Perform any necessary logout actions, such as clearing session data, tokens, or local storage.
      // For simplicity, we will redirect to the admin login page.
      localStorage.removeItem("access_token");
      this.$router.push({ name: "Login" });
    },

    initShowForm() {
      this.addShowForm.title = "";
      this.addShowForm.genre = "";
      this.addShowForm.date = "";
      this.addShowForm.time = "";
      this.addShowForm.venue = "";
      this.addShowForm.num_tickets = "";
      this.editShowForm.id = "";
      this.editShowForm.title = "";
      this.editShowForm.genre = "";
      this.editShowForm.date = "";
      this.editShowForm.time = "";
      this.editShowForm.venue = "";
      this.editShowForm.num_tickets = "";
    },
    initVenueForm() {
      this.addVenueForm.theatre = "";
      this.addVenueForm.place = "";
      this.addVenueForm.city = "";
      this.editVenueForm.id = "";
      this.editVenueForm.theatre = "";
      this.editVenueForm.place = "";
      this.editVenueForm.city = "";
    },

    onReset(e) {
      e.preventDefault();
      this.initForm();
    },
    onResetUpdate(e) {
      e.preventDefault();
      this.$refs.editShowModal.hide();
    },

    onSearch(e) {
      e.preventDefault();
      if (this.searchKeyword.trim() === "") {
        // If the search keyword is empty, reset the shows list to show all shows
        this.getShows();
      } else {
        // Filter the shows list based on the search keyword
        this.shows = this.shows.filter((show) =>
          show.title
            .toLowerCase()
            .includes(this.searchKeyword.trim().toLowerCase())
        );
      }
      this.searchKeyword = ""; // Reset the search input after searching
    },
  },

  created() {
    let token = localStorage.getItem("access_token");
    if (token == null) {
      this.$router.push("/login");
    } else {
      this.token = token;
    }
    this.getShows();
    this.getVenues();
  },
};
</script>
