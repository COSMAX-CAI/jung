<template>
    <button type="button" class="btn btn-primary m-2"
        data-bs-toggle="modal"
        data-bs-target="#exampleModal"
        @click="addClick()">
        키워드 추가
    </button>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>
                    키워드
                </th>
                <th>
                    삭제
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="kw in keywords" :key="kw.id">
                <td>
                    {{kw.keyword}}
                </td>
                <td>
                    <button type="button" class="btn btn-light mr-1"
                        @click ="deleteClick(kw.id)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                        </svg>
                    </button>
                </td>
            </tr>
        </tbody>
    </table>

    <div class="modal fade" id="exampleModal" tabindex="-1"
        aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">
                        키워드 생성
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                        aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="input-group mb-3">
                        <span class="iniput-group-text">키워드</span>
                        <input type="text" class="form-control" v-model="keywordToCreate" />
                    </div>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                        @click="createClick()">
                        생성
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'KeywordView',
  data() {
    return {
      keywords: [],
      keywordToCreate: [],
    };
  },
  methods: {
    refreshData() {
        axios.get("http://localhost:8000/keywords/?format=json")
            .then((response) => {
            this.keywords = response.data
        })
    },

    deleteClick(id){
        if(!confirm("정말 지우시겠습니까?")){
            return;
        }

        axios.delete("http://localhost:8000/keywords/"+ id +"/?format=json")
            .then(() => {
            alert("삭제하였습니다.")
            this.refreshData()
        })        
    },

    addClick(){
        this.keywordToCreate=""
    },

    createClick(){
            axios.post("http://localhost:8000/keywords/?format=json",
                {
                    keyword: this.keywordToCreate
                })
                .then(() => {
                    alert("생성하였습니다.") 
                    this.refreshData()
            })
    }
},
  mounted:function() {
    this.refreshData()
  }
}
</script>
