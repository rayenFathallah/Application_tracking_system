<template>
    <div>
      <section>
        <h1>Add a new job : </h1>
        <hr/><br/>
  
        <form @submit.prevent="submit">
          <div class="mb-3">
            <label for="title" class="form-label">Title:</label>
            <input type="text" name="title" v-model="form.title" class="form-control" />
          </div>
          <div class="mb-3">
            <label for="content" class="form-label">Description:</label>
            <textarea
              name="content"
              v-model="form.content"
              class="form-control description"
            ></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </section>
  
      <br/><br/>
  
      <section>
        <h1>Jobs</h1>
        <hr/><br/>
  
        <div v-if="jobs" class="container">
          <div class="row">
          <div v-for="job in jobs" :key="job.str_id" class="notes col-md-4 col-sm-6">
            <div class="card job-card" style="width: 18rem;">
              <div class="card-body">
                <div>
                  <div class="job_status" v-bind:style= "{ backgroundColor: job.open ? '#73B030' : 'red' }">{{ job.open ? "open"  : "closed" }}</div>
                  <div class ="job_title"> {{ job.title }}</div>
                  <p class="job-description"> {{ trim(job.text) }}</p>
                  <button class="arrow-button" @click="goToResumesPage(job)" >Check resumes<span class="arrow"></span></button>
                </div>
              </div>
            </div>
            <br/>
          </div>
        </div>
        </div>
  
        <div v-else>
          <p>Nothing to see. Check back later.</p>
        </div>
      </section>
    </div>
  </template>
  <style> 
  @import "@/styles/style.css";
  
  
</style>
  
  <script>
  import { defineComponent } from 'vue';
  import Swal from "sweetalert2";
  import { mapGetters, mapActions } from 'vuex';
  
  export default defineComponent({
    name: 'Dashboard_view',
    data() {
      return {
        form: {
          title: '',
          content: '',
        },
      };
    },
    created: function() {
      return this.$store.dispatch('get_all_jobs');

    },
    computed: {
      ...mapGetters({ jobs: 'stateJobs'}),
    },
    methods: {
      ...mapActions(['createJob']),
      async submit() {
        //await this.createJob(this.form);
        await this.createJob({"title" : this.form.title,"decsription": this.form.content}); 
        Swal.fire("Job added successfully");
        this.form.title = ''; 
        this.form.content = '';
      },
      goToResumesPage(selected_job) {
        this.$store.dispatch('setSelectedJob',selected_job);
        this.$router.push({ path: '/resumes'});
        console.log("went to page");
    },
      trim(text) {
        const words = text.split(/\s+/); // Split by whitespace
        const first50Words = words.slice(0, 50).join(' ');
        const result = first50Words + " ..."
        return result;
      }, 

    },
  });
  </script>