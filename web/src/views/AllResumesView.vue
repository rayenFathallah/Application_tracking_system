<template class="wrapper">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet">
<section>
    <form action="#" class>
<div class="g-2 row">
<div class="col-lg-3">
<div>Nom du candidat : </div>
<div class="filler-job-form">
<i class="uil uil-briefcase-alt"></i><input id="exampleFormControlInput1" placeholder="Candidate name " type="search" class="form-control filler-job-input-box form-control" />
</div>
</div>
<div class="col-lg-3">
<div>Etablissement : </div>
<div class="filler-job-form">
<i class="uil uil-location-point"></i>
<select class="form-select selectForm__inner" data-trigger="true" name="choices-single-location" id="choices-single-location" aria-label="Default select example" v-model="this.data.selected_institute">
<option v-for=" inst in this.data.institutes" :key="inst" v-bind:value="inst">{{ inst }}</option>

</select>
</div>
</div>
<div class="col-lg-3">
<div>Niveau : </div>
<div class="filler-job-form">
<i class="uil uil-clipboard-notes"></i>
<select class="form-select selectForm__inner" data-trigger="true" name="choices-single-categories" id="choices-single-categories" aria-label="Default select example" v-model="this.data.selected_niveau" placeholder="Niveau">
    <option v-for=" niv in this.data.niveaux" :key="niv" v-bind:value="niv">{{ niv }}</option>


</select>
</div>
</div>
<div class="col-lg-3">
<div>Etat : </div>
<div class="filler-job-form">
<i class="uil uil-clipboard-notes"></i>
<select  class="form-select selectForm__inner " data-trigger="true" aria-label="Default select example" v-model="this.data.selected_status">
    <option v-for="stat in this.data.status" :key="stat" v-bind:value="stat">{{ stat }}</option>
</select>
</div>
</div>
<div class="col-lg-3 adjust_margin">
<div>
<a class="btn btn-primary " @click="filter_resumes"><i class="uil uil-filter"></i> Filter</a><a class="btn btn-success ms-2" href="#" @click="resetUsers"><i class="uil uil-cog"></i>Reset filters</a>
</div>
</div>
</div>

</form>

    <div class="candidate-list">
    <div v-for="resume in this.data.filtered_resumes" :key="resume.name" class="notes">
    <div class="candidate-list-box card mt-4">
        <div class="p-4 card-body">
            <div class="align-items-center row">
                <div class="col-auto">
                    <div class="candidate-list-images">
                    <a href="#"><img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt class="avatar-md img-thumbnail rounded-circle" /></a>
                    </div>
                </div>
            <div class="col-lg-5">
                <div class="candidate-list-content mt-3 mt-lg-0">
                    <h5 class="fs-19 mb-0">
                    <a class="primary-link" href="#" v-on:click="dataURItoBlob(resume['binary']['$binary'])">{{resume['name']}}</a>
                    </h5>
                    <ul class="list-inline mb-0 text-muted"><strong> Education : </strong>
                        <li v-for="inst in  resume['infos']['education']['exact_institute']" :key="inst" ><i class="mdi mdi-map-marker"></i><strong>Etablissement : </strong>{{ inst }}</li>
                        
                        <li v-for="niv  in  resume['infos']['education']['niveau_exacte']" :key="niv" ><i class="mdi mdi-map-marker"></i><strong>Niveau : </strong>{{ niv }}</li>
                    </ul>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="mt-2 mt-lg-0 d-flex flex-wrap align-items-start gap-1">
                    <span  v-for="skill in  resume['infos']['skills']" :key="skill" class="badge bg-soft-secondary fs-14 mt-1">{{ skill }}</span>
                </div>
            </div>
            <div class="col-lg-3 d-flex trigger-item">
                <button class="button-48" role="button" @click="validate_change(resume['status'],resume['str_id'])"><span class="text">Change status</span></button>
                <select class="form-select selectForm__inner status" data-trigger="true" aria-label="Default select example" v-model="resume['status']" v-bind:style= "{ backgroundColor: resume['status'] === 'waiting' ? '#cccccc' : resume['status'] === 'interviewing' ? 'orange' : resume['status'] === 'rejected' ? 'red' : resume['status'] === 'accepted' ? '#00ff91a6' : 'orange' }">
                <option v-for="stat in this.data.status" :key="stat" v-bind:value="stat">{{ stat }}</option>
                </select>
            </div>
        </div>
        <div class="favorite-icon">
            <a href="#"><i class="mdi mdi-heart fs-18"></i></a>
        </div>
        </div>
        </div>
    </div>
    </div>


</section>
  </template>
<style type="text/css">
  @import "@/styles/style.css";
  .adjust_margin {
    margin-bottom: 20px;
    
  }

</style>

	
  <script>
  import { defineComponent } from 'vue';
  //import { mapGetters } from 'vuex';
  import Swal from "sweetalert2";

  
  export default defineComponent({
    name: 'all_resumes_view',

    data() {
  return {
    data: {
      resumes: [],
      institutes:[] ,
      selected_institute :"",
      selected_niveau : "",
      selected_status : "",
      filtered_resumes : [],
      status : ['interviewing','accepted','waiting','shortlisted','rejected'],
      niveaux : ["ingenieurie",'licence','mastere','preparatoire','doctorat'], 


    }
  };
},
    async created() {

    
    try {
        const my_resumes = await this.$store.dispatch('get_all_resumes', {"str_id": ""});
        const my_institutes = await this.$store.dispatch('get_all_institutes');
        this.data.institutes = my_institutes;
        this.data.resumes = my_resumes;
        this.data.resumes.sort((a, b) => b['score'] - a['score']);
        this.data.filtered_resumes =this.data.resumes ;
    } catch (error) {
        console.error("Error in created:", error);
    }
    },


    methods: {
        async get_all_resumes() {
        const my_resumes = await this.$store.dispatch('get_all_resumes',{"str_id": ""});
        this.data.filtered_resumes = my_resumes;
        this.data.filtered_resumes.sort((a, b) => b['score'] - a['score']);

      },
        dataURItoBlob(dataURI) {
            const byteString = window.atob(dataURI);
            const arrayBuffer = new ArrayBuffer(byteString.length);
            const int8Array = new Uint8Array(arrayBuffer);
            for (let i = 0; i < byteString.length; i++) {
                int8Array[i] = byteString.charCodeAt(i);
            }
            const blob = new Blob([int8Array], { type: 'application/pdf'});
            const url = URL.createObjectURL(blob);

// to open the PDF in a new window
            window.open(url, '_blank');
            return blob;
            },
            resetUsers() {
                this.data.filtered_resumes = this.data.resumes;
                this.data.selected_institute =""; 
                this.data.selected_niveau="";
                this.data.selected_status="";
            },
            filter_resumes() {
                this.data.filtered_resumes = this.filterUsers;

            },

            async validate_change(new_status,resume_id) {
                try {
                    await this.$store.dispatch('updateResume', {"new_status":new_status,"resume_id":resume_id});
                    Swal.fire("Candidate status updated successfully!");

                }
                catch {
                    console.error('problem while updating the status')

                }

            },
            filterCandidates1(resumes) {
            return resumes.filter(resume => {
            if (this.data.selected_institute || this.data.selected_institute > 0 ) {
                return resume['infos']['education']['exact_institute'].includes(this.data.selected_institute);
            } else {
                return true;
            }
            });

            },
            filterCandidates2(resumes) {
                return resumes.filter(resume => {
                if (this.data.selected_niveau || this.data.selected_niveau.length > 0 ) {
                    return resume['infos']['education']['niveau_exacte'].includes(this.data.selected_niveau);
                } else {
                    return true;
                }
                });
            },
            filterCandidates3(resumes) {
                return resumes.filter(resume => {
                if (this.data.selected_status || this.data.selected_status.length > 0 ) {
                    return resume['status']==this.data.selected_status;
                } else {
                    return true;
                }
                });
            },

  },
  computed: {
    filterCandidates() {
        return this.data.resumes.filter(resume => {
            if((this.data.selected_institute && this.data.selected_niveau && this.data.selected_status) || (this.data.selected_institute.length > 0 && this.data.selected_niveau.length > 0 && this.data.selected_status > 0)){
      return resume['infos']['education']['exact_institute'].includes(this.data.selected_institute) && resume['infos']['education']['niveau_exacte'].includes(this.data.selected_niveau);

            }
            else if(this.data.selected_institute || this.data.selected_institute.length > 0){
                return resume['infos']['education']['exact_institute'].includes(this.data.selected_institute);
            }
            else if(this.data.selected_niveau || this.data.selected_niveau.length > 0){

                return resume['infos']['education']['niveau_exacte'].includes(this.data.selected_niveau);
            }
            else {
                return resume;
            }
        });
      },
      filterUsers() {
        let filteredResumes = this.data.resumes;

// Apply the filters
        filteredResumes = this.filterCandidates1(filteredResumes);
        filteredResumes = this.filterCandidates2(filteredResumes);
        filteredResumes = this.filterCandidates3(filteredResumes);
        return filteredResumes
      },




    },  
    mounted() {
    // Load jQuery script
    const jqueryScript = document.createElement('script');
    jqueryScript.src = 'https://code.jquery.com/jquery-1.10.2.min.js';
    document.head.appendChild(jqueryScript);

    // Load Bootstrap bundle script
    const bootstrapScript = document.createElement('script');
    bootstrapScript.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js';
    document.head.appendChild(bootstrapScript);
  }
  });

  </script>