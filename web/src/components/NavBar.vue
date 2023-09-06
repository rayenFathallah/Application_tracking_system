<template>
    <header>
      <nav class="navbar navbar-expand-md red_bg">
        <div class="container">
          <img src="@/assets/logo.png"  class="navbar-brand nav_img" alt="Logo" />
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul v-if="isLoggedIn" class="navbar-nav me-auto mb-2 mb-md-0">
              <li class="nav-item"> 
                <router-link class="nav-link linkk" to="/dashboard">Dashboard</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link linkk" to="/all_resumes">All candidates</router-link>
              </li>

            </ul>
            <ul v-else class="navbar-nav me-auto mb-2 mb-md-0">
              <li class="nav-item">
                <router-link class="nav-link linkk" to="/">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link linkk" to="/register">Register</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link linkk" to="/login">Log In</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

  </template>
  <style>
    .red_bg {
      background-color : #D33E46;
    }
    .nav_img {
      height : 70px;
    }
    .linkk {
      color : white;
    }
  </style>
  <script>
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    name: 'NavBar',
    computed: {
      isLoggedIn: function() {
        return true
      }
    },
    methods: {
      async logout () {
        console.log("logged out");
      }
    },
  });
  </script>
  
  <style scoped>
  a {
    cursor: pointer;
  }
  </style>