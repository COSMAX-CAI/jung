import pymongo
from pymongo import MongoClient
from sqlite3 import Timestamp
import datetime
import json

cluster = MongoClient("mongodb://root:example@localhost/")
print("hi", cluster)

db = cluster["patent_project"]
collection = db["crawling_keywords"]

def get_oldest_keyword():
   global collection
   results1=collection.find({}).limit(1)

   # 한번도 크롤링한 적이 없는 키워드를 크롤링한다.
   results=collection.find({"last_crawling": None}).limit(1)
   print("hi2", results)
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
print("hi3", to_crawl)

#for x in results:
#    print(x)

