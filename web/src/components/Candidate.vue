<template>
<div>hi</div>
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
                    <a class="primary-link" href="#">{{resume['name']}}</a><span class="badge bg-success ms-1"><i class="mdi mdi-star align-middle"></i>{{resume['score']}}</span>
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
        </div>
        <div class="favorite-icon">
            <a href="#"><i class="mdi mdi-heart fs-18"></i></a>
        </div>
        </div>
        </div>
  </template>
  
  <script>
  import { defineComponent } from 'vue';

  
  export default defineComponent({
    props: {
    resume: Object
    },
    
    name: 'Candidate_template',
    data() {
      return {
        
      };
    },
    created: function() {
        console.log("yes I am created");
    },


  });
  </script>