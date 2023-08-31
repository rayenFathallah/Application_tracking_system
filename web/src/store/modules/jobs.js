import axios from 'axios';

const state = {
  jobs: null,
  job: null
};

const getters = {
  stateJobs: state => state.jobs,
  stateJob: state => state.job,
};

const actions = {
  async createJob({dispatch},job) {
        //await dispatch('get_all_jobs');
        console.log(job['decsription']);
        console.log(job['title']);
        const response = await axios.post('/post_job', {'title':job['title'],'description':job['decsription']});
        console.log(response.data);
        await dispatch('get_all_jobs');
  },

  async get_all_jobs({commit}) {
    let {data} = await axios.get('/get_jobs');
    commit('setJobs', JSON.parse(data));
  },


  async setSelectedJob({ commit }, selectedJob) {
    console.log("job set successfully"); 
    commit('setJob', selectedJob);
  },


  async viewJob({commit}, id) {
    let {data} = await axios.get(`/get_job/${id}`);
    commit('setJob', JSON.parse(data));
  },
  // eslint-disable-next-line no-empty-pattern
  async updateJob({}, id,new_job) {
    await axios.put(`/update_job/${id}`, new_job);
  },
  // eslint-disable-next-line no-empty-pattern

};

const mutations = {
  setJobs(state, jobs){
    state.jobs = jobs;
  },
  setJob(state, job){
    state.job = job;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};