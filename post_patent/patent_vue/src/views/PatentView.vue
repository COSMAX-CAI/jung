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

  <a v-if="prev_page != null" @click="setUrl(prev_page, -1)" href="#">
      &#60;
  </a>
  <a @click="gotoPage(2)" href="#">
      {{page_number +1 }}
  </a>
  <a v-if="next_page != null" @click="setUrl(next_page, 1)" href="#">
      &#62;
  </a>

  <div v-for="(pat, idx) in patents" :key="pat.app_number">
      <ul>
          <div>{{ idx + 1 + page_number*10}}
            <img v-if="pat.drawing !== null" v-bind:src="pat.drawing"  alt="" width="150" height="150">
              <br> 제목 : {{ pat.title }} ({{pat.app_name}}) <br> 등록상태 : {{ pat.reg_status }} <br> 설명 : {{ pat.astr_cont }}
              <br>
                  <button type="button" class="btn btn-light mr-1"
                  data-bs-toggle="modal"
                  data-bs-target="#exampleModal"
                  @click="modifyClick(pat)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                    <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
                  </svg>
                  
                </button>
                <button type="button" class="btn btn-light mr-1"
                  @click="deleteClick(pat.app_number)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                    <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                  </svg>
                </button>
          </div>
      </ul>
  </div>
  

  <div class="modal fade" id="exampleModal" tabindex="-1"
      arialabelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-centered">
          <div class="modal-content">
              <div class="modal-header">
                  <h5 class="modal-title" id="exampleModalLabel">
                      {{modalTitle}}
                  </h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal"
                      aria-label="Close"></button>
              </div>
              <div v-if="cur_pat != null" class="modal-body">
                제목 : {{ cur_pat.title }} ({{cur_pat.app_name}}) <br> 등록상태 : {{ cur_pat.reg_status }} <br>
                출원번호: {{cur_pat.app_number}} ({{cur_pat.app_date}})<br>
                공개번호: {{cur_pat.open_number == null ? '-' : (cur_pat.open_number + '(' + cur_pat.open_date + ')')}}<br>
                출판번호: {{cur_pat.pub_number == null ? '-' : (cur_pat.pub_number + '(' + cur_pat.pub_date + ')')}}<br>
                등록번호: {{cur_pat.reg_number == null ? '-' : (cur_pat.reg_number + '(' + cur_pat.reg_date + ')')}}<br>
                설명 : {{ cur_pat.astrt_cont }}
                <br> 
                  <div v-for="(rkw,index) in cur_pat.keywords" :key="rkw" class="input-group mb-3">
                      <span class="input-group-text">키워드 {{index + 1}}</span>
                      <select class="form-select" v-model="cur_pat.keywords[index]" @change="keywordChanged">
                          <option v-for="kw in keywords" :key="kw.id">
                              {{kw.keyword}}
                          </option>
                          <option key="">
                          </option>
                      </select>
                  </div>
                  <div class="input-group mb-3">
                      <span class="input-group-text">추가할 키워드</span>
                      <select class="form-select" v-model="regKeywordToAdd" @change="keywordAdded">
                          <option v-for="kw in keywords" :key="kw.id">
                              {{kw.keyword}}
                          </option>
                          <option key="">
                          </option>
                      </select>
                  </div>
                  <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                      @click="updateClick()">
                      키워드 수정
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
            
            keywords: [],

            searchKeyword: "전체",
            
            modalTitle: "",
            cur_pat: null,
            prev_page: null,
            next_page: null,
            cur_url: null,
            page_number: 0
        };
    },
    methods: {
        processResponse(response) {
            this.patents = response.data.results;
            this.prev_page = response.data.previous;
            this.next_page = response.data.next;

        },
        refreshData() {
            if(this.cur_url == null) {
                if(this.searchKeyword === "" || this.searchKeyword === "전체") {
                    this.cur_url = "http://localhost:8000/patents/?format=json"
                } else {
                    this.cur_url = "http://localhost:8000/patents/"+this.searchKeyword+"/keyword/?format=json";
                }
                this.page_number = 0;
            }

            axios.get(this.cur_url)
                    .then((response) => {
                        this.processResponse(response)
                    })
            axios.get("http://localhost:8000/keywords/?format=json")
                .then((response) => {
                    this.keywords = response.data.results
                })
        },
        setUrl(url, inc) {
            this.cur_url = url;
            this.page_number += inc;
            this.refreshData();
        },
        gotoPage(page_number) {
            this.page_number = page_number;
            if(this.searchKeyword === "" || this.searchKeyword === "전체") {
                this.cur_url = "http://localhost:8000/patents/?format=json&page="+page_number;
                } else {
                    this.cur_url = "http://localhost:8000/patents/"+this.searchKeyword+"/keyword/?format=json&page="+page_number;
                }

            this.refreshData();
        },
        search() {
            this.cur_url = null;
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
        modifyClick(pat) {
            this.modalTitle = "특허 상세"

            this.cur_pat = pat
        },
        keywordAdded() {
            this.cur_pat.keywords.push(this.regKeywordToAdd)
            this.regKeywordToAdd = ""
        },
        keywordChanged() {
            this.cur_pat.keywords = this.cur_pat.keywords.filter(kw => kw !== "")
        },
        updateClick() {
            axios.put("http://localhost:8000/patents/"+this.cur_pat.app_number+"/?format=json",
                this.cur_pat)
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
