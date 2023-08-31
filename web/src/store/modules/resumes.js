import axios from 'axios';

const state = {
  resumes: null,
  resume: null,
  all_resumes : null,
};

const getters = {
  stateResumes: state => state.resumes,
  stateResume: state => state.resume,
  stateAllResumes : state => state.all_resumes
};

const actions = {
  async get_all_resumes({commit},job) {
    if(state.all_resumes!=null && job['str_id']=="") {
      const data = state.all_resumes; 
      commit('setResumes', data);
      return data;
    }
    else {
      const startTime = performance.now();
      const {data} = await axios.put('/get_all_resumes2',job);
      const endTime = performance.now();
// Calculate the elapsed time in milliseconds
      const elapsedMilliseconds = endTime - startTime;
      console.log(elapsedMilliseconds);
      commit('setResumes', JSON.parse(data));
      commit('setAllResumes',JSON.parse(data));  
      const parsedData = JSON.parse(data);
      return parsedData;
    }

  },
  async viewResume({commit}, id) {
    let {data} = await axios.get(`/resume/${id}`);
    commit('setResume', data);
  },
  async get_all_institutes() {
    let {data} = await axios.get('/get_institutes');
    return data;
  },
  async get_all_niveaux() {
    let {data} = await axios.get('/get_niveaux');
    const parsedData = JSON.parse(data);

    return parsedData;
  },
  /*
  async get_job_resumes({commit},job) {
    let {data} = await axios.put('/get_job_resumes',job);
    commit('setResumes', JSON.parse(data));
    return JSON.parse(data)
  },
  */
  async get_job_resumes({ commit }, job) {
    try {
      const { data } = await axios.put('/get_job_resumes', job);
      const parsedData = JSON.parse(data);
      commit('setResumes', parsedData);
      return parsedData;
    } catch (error) {
      console.error("Error in get_job_resumes:", error);
      throw error;
    }
  },

  // eslint-disable-next-line no-empty-pattern
  async updateResume({},update) {
    try {
      await axios.put('/update_candidate_status', {'new_status':update['new_status'],'resume_id':update['resume_id'],'job_id':update['job_id']});
      const indexToUpdate = state.all_resumes.findIndex(item => item['str_id'] === update['resume_id']);
      state.all_resumes[indexToUpdate]["status"] = update['new_status'];

    } 
    catch {
      console.error("error while updating the status")
    }
  },
  // eslint-disable-next-line no-empty-pattern

};

const mutations = {
  setResumes(state, resumes){
    state.resumes = resumes;
  },
  setResume(state, resume){
    state.resume = resume;
  },
  setAllResumes(state,all_resumes){
    state.all_resumes = all_resumes;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};