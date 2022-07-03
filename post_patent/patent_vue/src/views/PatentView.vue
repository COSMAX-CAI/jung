<template>
  <div class="input-group mb-3">
    <span class="input-group-text">키워드 검색</span>
    <select class="form-select" v-model="searchKeyword" @change="search">
        <option>
            전체
        </option>    
        <option v-for="kw in keywords" :key="kw.id">
            {{kw.keyword}}
        </option>
    </select>    
  </div>
  <button type="button" class="btn btn-primary m-2"
    data-bs-toggle="modal"
    data-bs-target="#exampleModal"
    @click="addClick()">
    특허 추가
  </button>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>
          출원번호
        </th>
        <th>
          특허명
        </th>
        <th>
          삭제
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="pat in patents" :key="pat.id">
        <td>
          {{pat.registration_number}}
        </td>
        <td>
          {{pat.title}}
        </td>
        <td>
          <button type="button" class="btn btn-light mr-1"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
            @click="modifyClick(pat.id)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
                <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
            </svg>
          </button>
          <button type="button" class="btn btn-light mr-1"
            @click="deleteClick(pat.id)">
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
    arialabelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="examplemodalLabel">
            {{modalTitle}}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"
            aria-label="Close">
          </button>
        </div>
        <div class="modal-body">
          <div class="input-group mb-3">
            <span class="input-group-text">출원번호</span>
            <input type="text" class="form-control" v-model="regNumber"/>
          </div>
        <div class="input-group mb-3">
            <span class="input-group-text">특허명</span>
            <input type="text" class="form-control" v-model="regTitle"/>
          </div>
        <div class="input-group mb-3">
            <span class="input-group-text">초록</span>
            <input type="text" class="form-control" v-model="regAbstract"/>
          </div>
        <div v-for="(rkw, index) in regKeywords" :key="rkw" class="input-group mb-3">
            <span class="input-group-text">키워드{{index+1}}</span>
            <select class="form-select" v-model="regKeywords[index]" @change="keywordChanged">
                <option v-for="kw in keywords" :key="kw.id">
                    {{kw.keyword}}
                </option>
            </select>
          </div>
        <div class="input-group mb-3">
            <span class="input-group-text">추가할 키워드</span>
            <select class="form-select" v-model="regKeywordToAdd" @change="keywordAdded">
                <option v-for="kw in keywords" :key="kw.id">
                    {{kw.keyword}}
                </option>
            </select>
          </div>          
          <button v-if="regId<0" type="button" class="btn btn-primary" data-bs-dismiss="modal"
            @click="createClick()">
            생성
          </button>          
          <button v-if="regId >= 0" type="button" class="btn btn-primary" data-bs-dismiss="modal"
            @click="updateClick()">
            수정
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
export default {
  name: 'PatentView',
  data() {
    return {
      patents: [],
      regId: -1,
      regNumber: "",
      regTitle: "",
      regAbstract: "",
      regKeywords: [],
      regKeywordToAdd: "",

      keywords: [],

      searchKeyword: "전체",

      modalTitle: "",
      
    };
  },
  methods: {
    refreshData() {
        console.log(this.keywordSearch)
        if(this.searchKeyword=== "" || this.searchKeyword === "전체" ){
            axios.get("http://localhost:8000/patents/?format=json")
            .then((response) => {
                this.patents = response.data
            })
        } else {
            axios.get("http://localhost:8000/patents/"+this.searchKeyword+"/keyword/?format=json")
            .then((response) => {
                this.patents = response.data
            })            
        }
        axios.get("http://localhost:8000/keywords/?format=json")
            .then((response) => {
            this.keywords = response.data
            this.keywords.push({id: -1, keyword:"키워드 제거"})
        })
    },
    search(){
        this.refreshData()
    },
    deleteClick(id) {
      if(!confirm("정말 지우시겠습니까?")) {
        return;
      }
      axios.delete("http://localhost:8000/patents/" + id + "/?format=json")
        .then(() => {
          alert("삭제하였습니다.")
          this.refreshData()
        })
    },
    addClick() {

        this.regId = -1

        this.regNumber=""
        this.regTitle=""
        this.regAbstract=""
        this.regKeywords=[]
        this.regKeywordToAdd=""

      this.modalTitle= "특허 추가"
    },
    createClick() {
      axios.post("http://localhost:8000/patents/?format=json",
      {
        registration_number : this.regNumber,
        title : this.regTitle,
        abstract : this.regAbstract,
        keywords : this.regKeywords
      })
        .then(() => {
          alert("생성하였습니다.")
          this.refreshData()
      })
    },
    modifyClick(id){
        this.modalTitle= "특허 수정"
        
        const patent = this.patents.find(pat => pat.id === id)

        this.regId = id

        this.regNumber=patent.registration_number
        this.regTitle=patent.title
        this.regAbstract=patent.abstract
        this.regKeywords=patent.keywords
    },
    keywordAdded(){
        this.regKeywords.push(this.regKeywordToAdd)
        this.regKeywordToAdd = ""
    },
    keywordChanged(){
        console.log("키워드변화")
        this.regKeywords = this.regKeywords.filter(kw => kw !== "키워드 제거")
    },
    updateClick() {
        axios.put("http://localhost:8000/patents/" + this.regId + "/?format=json",
            {
                registration_number : this.regNumber,
                title : this.regTitle,
                abstract : this.regAbstract,
                keywords : this.regKeywords
            })
            .then(() => {
                alert("수정하였습니다.")
                this.refreshData()
            })
    }
  },
  mounted:function() {
    this.refreshData()
  }
}
</script>