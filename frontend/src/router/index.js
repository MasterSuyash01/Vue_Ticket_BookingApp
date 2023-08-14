import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import AdminDashboard from "../components/AdminDashboard.vue";
import LoginView from "../components/LoginView.vue";
import UserRegistration from "../components/UserRegistration.vue";
import BookingView from "../components/BookingView.vue"; // Import the Booking component
import UserDashboard from "../components/UserDashboard.vue"; // Import the Booking component

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/admin/dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
  },
  {
    path: "/user/registration",
    name: "UserRegistration",
    component: UserRegistration,
  },
  {
    path: "/user/booking", // Add the new path for the Booking component
    name: "Booking",
    component: BookingView,
  },
  {
    path: "/user/dashboard", // Add the new path for the Booking component
    name: "UserDashboard",
    component: UserDashboard,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
