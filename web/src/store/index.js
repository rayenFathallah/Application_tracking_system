import { createStore } from "vuex";

import jobs from './modules/jobs';
import resumes from './modules/resumes';

export default createStore({
  modules: {
    jobs,
    resumes,
  }
});