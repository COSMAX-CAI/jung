import pymongo
from pymongo import MongoClient
from sqlite3 import Timestamp
import datetime
import json
import os
import dotenv
import sys

def load_config_file():
   with open("../crawl.conf", "r") as conf_file:
      return json.load(conf_file)

def get_oldest_keyword(conf):
   # udpate되지 않은 것 먼저
   result = keywords_db_collection.find_one({"updated": None})
   if result != None:
      return result

   pivot_days = conf.get('pivot_days', 30)
   oneMonthAgo = datetime.datetime.now() - datetime.timedelta(days=pivot_days)
   results = keywords_db_collection.find({'updated': {"$lt": oneMonthAgo}}).sort("updated",1).limit(1)

   for item in results:
      return item
   
   #results에 아무것도 없을 때 return None
   return None

# main문으로 실행 될 때만
if __name__ == "__main__":
   # 암호는 환경 변수로 로드하는 것이 좋다 -> .env에 저장
   # 환경변수 로드하기
   dotenv.load_dotenv(verbose=True)

   # 설정 파일 불러오기
   conf = load_config_file()

   # mongoDB 초기화
   mongo_user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
   mongo_password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

   cluster = MongoClient("mongodb://{mongo_user}:{mongo_password}@localhost/")

   print(cluster)
   print(mongo_user)
   print(mongo_password) 

   db = cluster["patent_project"]
   keywords_db_collection = db["crawling_keywords"]

   # results1=keywords_db_collection.find({}).limit(1)
   # print(results1)

   # a = keywords_db_collection.find_one({})
   # print("a",a)

   keywords_per_day = conf.get('keywords_per_day', 1)
   print(keywords_per_day)
   for idx in range(0, keywords_per_day):
      keyword = get_oldest_keyword(conf)
      print(keyword)
      if keyword == None :
         print("No more keyword remained")
         sys.exit(0)

      print(keyword)

   # 한번도 가져오지 않은거 -> 가장 마지막으로 성공했던 키워드 가져오기 (정책) - 저번주에 만든 last_crawling 삭제
   # result = collection.find_one({})
   # print(result)