## ⚖ Patent API

### 프로젝트 일정
| Week | 세미나 | 과제 | 내용 |
| ------ | -- | -- |----------- |
| 1주차(5/13) | ☑️ | ☑️ | Patent API 관련하여 내용 공유 및 프로젝트 준비 |
| 2주차(5/20) | ☑️ | ☑️ | 1주차 과제 공유 및 MongoDB 사용해보기 |
| 3주차(5/27) | ☑️ | ☑️ | MongoDB에 API 데이터 저장하기 |
| 4주차(6/10) | ☑️ |  | PostgreSQL & Django 사용해보기 |
| 5주차(6/17) | ☑️ |  | 프론트엔드(Vue.js) 구현 & Django 연결 |
| 6주차(7/1) | ☑️ |  | 프론트엔드(Vue.js) 구현 |
| 7주차(7/8) | ☑️ |  | PostgreSQL에 API 데이터 저장 & Djang 모델 |
| 8주차(7/29) | ☑️ |  ||
| 9주차(8/05) | ☑️ |  ||

----------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 주차 상세 내용
+ 1주차: 프로젝트 설명 및 공유
+ 2주차: Docker를 사용하여 MongoDB 설치 & 사용하기
  + Docker Hub에서 Mongo 도커 이미지 pulll 받기
  
          docker pull mongo
  
  + MongoDB 컨테이너 생성
    + 'docker-compose.yml' 파일 생성
    
          version: '3.1'
          # 서비스명
          services:
          mongo:
            # 사용할 이미지
            image: mongo
            # 컨테이너 실행 시 재시작
            restart: always
            # 접근 포트 설정 (컨테이너 외부:컨테이너 내부)
            ports:
              - "27017:2701
            # -e 옵션
            environment:
              MONGO_INITDB_ROOT_USERNAME: root
              MONGO_INITDB_ROOT_PASSWORD: example

          mongo-express:
            image: mongo-express
            restart: always
            ports:
              - 8081:8081
            environment:
              ME_CONFIG_MONGODB_ADMINUSERNAME: root
              ME_CONFIG_MONGODB_ADMINPASSWORD: example
              ME_CONFIG_MONGODB_URL: mongodb://root:example@mongo:27017/
     + yml 파일을 생성한 디렉토리에서 docker-compose 명령어 실행
          
            docker-compose up -d
  + MongoDB 클라이언트로 데이터 저장
    + MongoExpress 접속
    
          http://localhost:8081/
          
    + Database 생성

          patent_project
          
          
    + Collection 생성

          crawling_keywords
      
    + New Document 생성
    
          {
              _id: ObjectId(),
              keyword: '화장료',
              created: Date(),
              last_crawling: {
                  crawling_date: Date(),
                  crawling_rows: 500,
                  total_rows: 1954
              }
          }
    
  + 파이썬으로 MongoDB 실행 및 DB 조회
    + 동일한 디렉토리에 crawl.py 파일 생성  
      
          import pymongo
          from pymongo import MongoClient
          from sqlite3 import Timestamp
          import datetime
          import json

          cluster = MongoClient("mongodb://root:example@localhost/")
          print(cluster)

          db = cluster["patent_project"]
          collection = db["crawling_keywords"]

          def get_oldest_keyword():
             global collection
             results1=collection.find({}).limit(1)

             # 한번도 크롤링한 적이 없는 키워드를 크롤링한다.
             results=collection.find({"last_crawling": None}).limit(1)
             result_list = list(results)

             #모두 crawling 한적이 있다면 가장 옛날에 크롤링한 녀석
             if len(list(results.clone()))== 0:
                #한달안에 크롤링한 녀석은 제외한다.
                oneMonthAgo = datetime.datetime.now()-datetime.timedelta(days=30)
                results = collection.find({"last_crawling.crawling_date": {"$lt":oneMonthAgo}}).sort("last_crawling.crawling_date", 1).limit(1)
                result_list = list(results)

             if len(result_list) == 0 :
                return None
             else:
                return result_list[0]

          #크롤링한 키워드를 가져 온다.
          to_crawl = get_oldest_keyword()
          print(to_crawl)
     + crawler 실행 후 데이터 확인
        
            python crawl.py 

+ 3주차
  + MongoDB Compass 설치 
  + [Code Link](/doc/220527_3주차.pdf)

+ 4주차(6/10)
  + PostSQL 설치
    + 사이트: https://www.postgresql.org/download/
    + SQL Shell
      + Password
      
            cailab_2022
            
      + Database 생성  
      
            create DATABASE patents;
        
      + Database 리스트 조회
      
            \list 
            
      + Database 선택
      
             \connect 데이터베이스 이름 -> \connect patents   
             
  + Django (주요 코드만 작성 & 세부 내용은 코드 참고)
    + 가상환경 접속
    
            (윈도우용) venv\Scripts\activate
            
    + Django 설치
    
           python -m pip install Django
      
    + 프로젝트 만들기
    
          django-admin startproject post_patent
      
    + 앱 생성(1)
    
          python manage.py startapp keywords


    + 앱 생성(2)

          python manage.py startapp patents


    + Rest Framework로 만들기

          https://www.django-rest-framework.org/api-guide/
          
    + 모델의 활성화(Migration)
    
          python manage.py makemigrations
          python manage.py migrate
        
    + 로컬에서 실행하기
    
          python manage.py runserver 
          
+ 5주차(6/17) 

  + Postman 설치
  
    + https://www.postman.com/downloads/
      + GET
          http://localhost:8000/patents/?format=json 
      + POST 
      + DELETE(5번째를 지우는 경우)
          http://localhost:8000/patents/5/?format=json 
  + Node js 설치
    + https://nodejs.org/ko/
    + npm 패키지 설치
    
          npm install -g <package>
  
  
   + Vue CLI
      + Vue CLI 설치
      
            npm install -g @vue/cli
            
      + Vue 프로젝트 생성(장고 프로젝트 폴더 열기)
      
            vue create patent vue
            
      + 실행하기
      
            npm run serve
            
  + Router
      + router 설치
      
            npm i vue-router@next
            
      + router 환경
      
            vue add router
        
  + Boostrap
    + https://bootstrap-vue.org/docs
    
          npm install vue bootstrap bootstrap-vue
     
    + main.js 에서 import 하기
    
          import "bootstrap/dist/css/bootstrap.min.css"
          import "bootstrap"
          
  + axios 설치(백엔드 서버와 통신하기 위해)
    + patent_vue 내 import 하기
     
           import axios from 'axios'
           
    + axios 설치
    
           npm install axios
  
  + CORS(Cross Domain 이슈 해결)
     + Django Settings.py 코드 추가
      
           INSTALLED_APPS -> 'corsheaders' 추가
           CORS_ORIGIN_ALLOW_ALL= True
           MIDDLEWARE ->  'corsheaders.middleware.CorsMiddleware' 추가
  
     + 패키지 설치
      
           pip install django-cors-headers
           python -m pip install django-cors-headers
  + 6주차(7/1)
     + patent_vue
        + KeywordView.vue 기능 추가
        + PatentView.vue 기능 추가
        
  + 7주차(7/8)
     + [장고] post_patent
        + patents 모델 수정
        + keywords 모델 수정
        
     + Postgre SQL
        + Table 생성 -> patents
        + crawl.py 작성
          + [Code Link](/doc/220708_7주차.pdf)
          
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 관련 링크
+ Docker Hub: https://hub.docker.com/_/mongo?tab=tags&page=1&ordering=last_updated
+ MongoDB Compass : https://www.mongodb.com/ko-kr/products/compass
+ PostSQL : https://www.postgresql.org/download/
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 자주 사용하는 코드

+ 가상환경 접속 : (윈도우용)

      venv\Scripts\activate
      
+ gitignore 업데이트 :
 
      git rm -r --cached . 
      git add .
      git commit -m "update gitignore"
