from sqlite3 import Timestamp
import pymongo
from pymongo import MongoClient
import datetime
import json


#json.dumps(x) 시, datetime.datetime() datetime.date() 면 json시리얼라이즈에러가 생김.
#이를 json.dumps(x, defalut = from_datetime_to_isoformat) 로 하거나
#json.dumps(x, defalut = str) 으로 하면 해결 됨.
def from_datetime_to_isoformat(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


cluster = MongoClient('mongodb://root:example@localhost/')
#print(cluster)


db = cluster["patent_project"]
collection = db["keywords"]

#한번도 크롤링한 적 없는 애들에 대해서 crawling 한다.

def check_crawling_date() : 
    global collection
    results = collection.find({"last_crawling" : None}).limit(1)
    for result in results:
        print("hi", result)
    print(len(list(results)))
    for x in results:
        print(json.dumps(x, default=str, indent=4, ensure_ascii=False))

    #print(results.explain())

    #모두 크롤링한 적이 있다면, 가장 옛날에 crawling한 녀석을 찾는다.
    if len(list(results)) == 0 :
        # 한달안에 crawling 한 녀석들은 제외한다.
        oneMonthago = datetime.datetime.now() - datetime.timedelta(days=30)
        db_curser = collection.find({"last_crawling.crawling_date" : {"$lt" : oneMonthago}}).sort("last_crawling.crawling_date", 1).limit(1)
        # curser (=커서) 는 DB를 한번 쭈욱 훑으면 사라짐! (리미트가 있을 경우, 리미트 만큼 가고 사라짐!)
        results_list = list(db_curser)
        
        for x in results_list :
            print(json.dumps(x, default=str, indent=4, ensure_ascii=False))
        
        print(results_list)
        
        if len(results_list) == 0 :
            return None
        else : 
            return results_list

to_crawl = check_crawling_date()

print(to_crawl)
