from ssl import OP_NO_COMPRESSION
import pymongo
from pymongo import MongoClient
import dotenv
import json
import os
import sys
from sqlite3 import Timestamp
import datetime
import urllib
import urllib.request
import xmltodict

def load_config_file():
    with open('crawl.conf', 'r') as conf_file:
        return json.load(conf_file)

def get_oldest_keyword(conf):
    result = keywords_db_collection.find_one({'updated': None})
    if result != None:
        return result
   
    pivotDays = conf.get('pivot_days', 30)
    oneMonthAgo = datetime.datetime.now() - datetime.timedelta(days=pivotDays)
    results = keywords_db_collection.find({"updated": {"$lt":oneMonthAgo}}) \
            .sort("updated", 1).limit(1)
    print("results", results)
    for item in results:
        print("item", item)
        return item

    #아무것도 없을 때
    return None

def extract_db_fields(item):
    fields = ['applicantName', 'applicationDate', 'applicationNumber', 'astrtCont', 'inventionTitle', 'registerDate', 'registerNumber', 'registerStatus']
    # 빈 dict 생성
    res = dict()
    for x in fields:
        res[x] = item[x]
    return res

def crawl_patent_iterator(keyword):
    client_key = os.getenv('KIPRIS_KEY')
    encText = urllib.parse.quote(keyword)

    current_page = 0
    total_count = -1
    number_of_rows = 10

    while total_count < 0 or current_page * number_of_rows <= total_count:

        current_page +=1 

        url = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getWordSearch?word=" + encText + f"&pageNo={current_page}&numOfRows={number_of_rows}"+ "&ServiceKey=" + client_key
        #print(url)

        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)

        if response.getcode() == 200:
            res_dict = xmltodict.parse(response.read().decode('utf-8'))
            print(res_dict)
            items = res_dict['response']['body']['items']['item']
            total_count = int(res_dict['response']['count']['totalCount'])
            for item in items:
                # yield 사용 
                yield extract_db_fields(item)
                #print(item)
        else: 
            print("Error Code", rescode)
            yield None

# 매칭되는 것을 저장
def store_in_db(item, keyword):
    # key값(출원번호)
    item['_id'] = item['applicationNumber']
    
    item_in_db = patents_db_collection.find_one({'_id': item['_id']})
    if item_in_db != None:
        if keyword in item_in_db['keywords']:
            print(f"{item['applicationNumber']} is not updated")
            return False #더이상 쿼리 안함
        else:
            new_keywords = item_in_db['keywords'] + keyword #새로운 키워드를 집어둠
            patents_db_collection.update_one({'_id':item['_id']}, {"$set": {'keywords': new_keywords}})
            print(f"{item['applicationNumber']} is updated")
            return True
    else: #item이 DB에 없다면 새롭게 집어넣음
        ### 여기 다시 보기(keywords, keyword 주의)###
        item['keywords'] = [keyword] #배열
        patents_db_collection.insert_one(item)
        print(f"{item['applicationNumber']} is updated")
        return True

# Dictionary로 되어있는 keyword 가 들어가있는 dict
def crawl_patents_into_db(keyword_in_db):

    keyword = keyword_in_db['keyword']

    incremental = keyword_in_db.get('completed', False)

    keywords_db_collection.update_one({'keyword': keyword}, {"$set": {"completed": False}})

    known_count = 0 
    accepting_known_patents = 50 #50개 이상 아는 것이 나오면 정지할 수 있다.
    # yield에서 반횐된것
    for item in crawl_patent_iterator(keyword):
        if item == None:
            print(f"{keyword} 검색중에 문제가 발생하였습니다.")
            sys.exit(1) #error는 1
        #print("main", item)  
        
        updated = store_in_db(item, keyword)
        if incremental:
            if not updated:
                known_count +=1
            else: 
                known_count = 0
            if known_count >= accepting_known_patents:
                break

    keywords_db_collection.update_one({'keyword': keyword}, {"$set": {"completed": True, "updated":datetime.datetime.now()}})
        


if __name__ == '__main__':
    # .env에 있는 환경변수 로드
    dotenv.load_dotenv(verbose=True)

    # 설정파일 불러오기
    conf = load_config_file()

    # mongoDB 초기화
    mongo_user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    mongo_password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

    cluster = MongoClient(f"mongodb://{mongo_user}:{mongo_password}@localhost/")
    print(mongo_user)
    print(mongo_password)
    print(cluster)


    db = cluster["patent_project"]
    keywords_db_collection = db["crawling_keywords"]
    patents_db_collection = db['patents']

    keywords_per_day = conf.get('keywords_per_day', 1)
    for idx in range(0, keywords_per_day):
        keyword = get_oldest_keyword(conf)
        print(keyword)
        if keyword == None:
            print("No more keyword remained")
            sys.exit(0)
        
        crawl_patents_into_db(keyword)
