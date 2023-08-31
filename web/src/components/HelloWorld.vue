<template>
  <div>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'component_one',
  data() {
    return {
      jobs: [],
    };
  },
  methods: {
    getMessage() {
      axios.get('/get_jobs')
        .then((res) => {
          this.jobs = res.data;
          console.log(res.data)
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    console.log("heyyy");
  },
};
</script>
