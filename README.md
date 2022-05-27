## ⚖ Patent API

### 프로젝트 일정
| Week | 세미나 | 과제 | 내용 |
| ------ | -- | -- |----------- |
| 1주차(5/07) | ☑️ | ☑️ | Patent API 관련하여 내용 공유 및 프로젝트 준비과정 진행 |
| 2주차(5/14) | ☑️ | ☑️ | 1주차 과제 공유 및 MongoDB 사용해보기 |
| 3주차(5/21) | ☑️ | ☑️ | |
| 4주차 | ☑️ | ☑️ | |
| 5주차 |  |  ||
| 6주차 |  |  ||
| 7주차 |  |  ||
| 8주차 |  |  ||

----------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 주차 상세 내용
+ 1주차
+ 2주차: Docker를 사용하여 MongoDB 설치 & 사용하기
  + Docker Hub에서 Mongo 도커 이미지 pulll 받기
  
          docker pull mongo
  
  + Mongodb 컨테이너 생성
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
          
            docker-compose up 
  + Crawler 생성
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
  
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
### 관련 링크

