#from ssl import OP_NO_COMPRESSION
import psycopg2
#import pymongo
#from pymongo import MongoClient
import dotenv
import json
import os
import sys
#from sqlite3 import Timestamp
import datetime
import urllib
import urllib.request
import xmltodict

def load_config_file():
    with open('crawl.conf', 'r') as conf_file:
        return json.load(conf_file)

def get_oldest_keyword(conf):

    cursor.execute(\
        '''SELECT keyword
            FROM keywords_keyword
            WHERE updated is NULL''')

    result = cursor.fetchone()

    print("여기", result)

    if result != None:
        return result
   
    pivotDays = conf.get('pivot_days', 30)
    oneMonthAgo = datetime.datetime.now() - datetime.timedelta(days=pivotDays)
    print("One Month ago", oneMonthAgo)

    cursor.execute(\
        '''SELECT keyword
            FROM keywords_keyword
            WHERE updated < (%s)
            ORDER BY updated ''', [oneMonthAgo])

    result = cursor.fetchone()
    print('Older than 30 days', result)
    # results = keywords_db_collection.find({"updated": {"$lt":oneMonthAgo}}) \
    #         .sort("updated", 1).limit(1)
    # print("results", results)
    # for item in results:
    #     print("item", item)
    #     return item

    #아무것도 없을 때
    return result

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

        hdr = {'Accept-Charset': 'utf-8'}
        request = urllib.request.Request(url, headers=hdr)
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
    app_number = item['applicationNumber']
    cursor.execute(
        '''SELECT keywords
            FROM patents_patent
            WHERE app_number = (%s)''',[app_number])

    item_in_db = cursor.fetchone()
    print('item in DB', item_in_db)
    
    if item_in_db != None:
        if keyword in item_in_db[0]:
            print(f"{item['applicationNumber']} is not updated")
            return False #더이상 쿼리 안함
        else:
            new_keywords = item_in_db[0] + [keyword] #새로운 키워드를 집어둠
            cusor.execute(
                '''UPDATE patents_patent
                    SET keywords = (%s)
                    WHERE app_number = (%s)''', [new_keywords, app_number])
            db.commit()
            # 다르게 바뀌는 내용들 pub date 등
            print(f"{item['applicationNumber']} is updated")
            return True

    else: #item이 DB에 없다면 새롭게 집어넣음
        ### 여기 다시 보기(keywords, keyword 주의)###
        print(item)
        cursor.execute(
            '''INSERT INTO patents_patent VALUES
                (%s, %s, %s, %s, %s, %s, %s,
                 %s, %s, %s, %s, %s, %s, %s, %s)''',
                 [
                    item['inventionTitle'],
                    [keyword],
                    item['applicationDate'],
                    item['applicantName'],
                    item['applicationNumber'],
                    item.get('astrtCont', None),
                    item.get('bigDrawing', None),
                    item.get('drawing', None),
                    item.get('openDate', None),
                    item.get('openNumber', None),
                    item.get('pubDate', None),
                    item.get('pubNumber', None),
                    item.get('registerDate', None),
                    item.get('registerNumber', None),
                    item.get('registerStatus', None)])
        db.commit()
        print(f"{item['applicationNumber']} is updated")
        return True

# Tuple 형태로 가지고 온다
def crawl_patents_into_db(keyword_in_db):
    # 화장료 키워드가 tuple 첫번쨰 꺼
    keyword = keyword_in_db[0]
    
    print('keyword', keyword)

    known_count = 0 
    accepting_known_patents = 50 #50개 이상 아는 것이 나오면 정지할 수 있다.
    # yield에서 반횐된것
    for item in crawl_patent_iterator(keyword):
        if item == None:
            print(f"{keyword} 검색중에 문제가 발생하였습니다.")
            sys.exit(1) #error는 1
        #print("main", item)  
        
        updated = store_in_db(item, keyword)

    # keywords_db_collection.update_one({'keyword': keyword}, {"$set": {"completed": True, "updated":datetime.datetime.now()}})
        


if __name__ == '__main__':
    # .env에 있는 환경변수 로드
    dotenv.load_dotenv(verbose=True)

    # 설정파일 불러오기
    conf = load_config_file()

    # DB 초기화
    db_user = os.getenv('DB_ROOT_USERNAME')
    db_password = os.getenv('DB_ROOT_PASSWORD')

    db = psycopg2.connect(host='localhost', dbname='patents', port=5432, user=db_user, password=db_password)
    cursor = db.cursor()

    keywords_per_day = conf.get('keywords_per_day', 1)

    for idx in range(0, keywords_per_day):
        keyword = get_oldest_keyword(conf)
        print('Oldest Keyword', keyword)
        if keyword == None:
            print("No more keyword remained")
            sys.exit(0)
        
        crawl_patents_into_db(keyword)
