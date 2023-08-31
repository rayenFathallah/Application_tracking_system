<template> 
    <div> 
        Just saying hi
    </div>
</template>
<script>
import axios from 'axios'; 
export default {
  name: 'jobs_component',
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
    this.getMessage();
  },
};
</script>