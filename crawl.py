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

# Json dictionary 형태로 넘어옴
def load_config_file():
    with open('crawl.conf', 'r') as conf_file:
        return json.load(conf_file)

# pivot_days보다 crawling한지 오래된 keyword 중 
# 가장 오래된 keyword를 반환
def get_oldest_keyword(conf):
    # crawling한 적이 없는 keyword가 있다면 이를 반환
    cursor.execute(\
        '''SELECT keyword
            FROM keywords_keyword
            WHERE updated is NULL''')

    # 맨앞에 하나 fetch(client로 넘어옴)
    # fetchmany는 배열로 넘어옴
    result = cursor.fetchone()

    print("Updated is NULL", result)

    if result != None:
        # 결과 반환
        return result
   
   # crawling한 적이 없는 keyword가 없다면
   # crawling history가 가장 오래된 keyword를 반환
   # 단, pivot_days보다는 crawling 한 적이 오래되어야 함
    pivotDays = conf.get('pivot_days', 30)
    oneMonthAgo = datetime.datetime.now() - datetime.timedelta(days=pivotDays)
    print("One Month ago", oneMonthAgo)
    cursor.execute(\
        '''SELECT keyword
            FROM keywords_keyword
            WHERE updated < (%s)
            ORDER BY updated ''', [oneMonthAgo]) #업데이트 순으로 나열. 반대는 DESC

    result = cursor.fetchone()
    print('Older than 30 days', result)

    #아무것도 없을 때
    return result

def extract_db_fields(item):
    fields = ['applicantName', 'applicationDate', 'applicationNumber', 'astrtCont', 'inventionTitle', 'registerDate', 'registerNumber', 'registerStatus']
    # 빈 dict 생성
    res = dict()
    for x in fields:
        res[x] = item[x]
    return res

# 특정 keyword에 대한 모든 특허를 iterate 
# 커다란 덩어리를 가져와서 yield, 받는 쪽은 for 안으로 가볍게 받음
def crawl_patent_iterator(keyword):
    client_key = os.getenv('KIPRIS_KEY')
    # print(client_key)
    # keyword encoding
    encText = urllib.parse.quote(keyword)

    current_page = 0
    total_count = -1 # 전체 몇개
    number_of_rows = 10 # 나중에 변경(한번에 가져올 수 있는 row 약 500개)

    while total_count < 0 or current_page * number_of_rows < total_count:

        current_page +=1 

        url = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getWordSearch?word=" + encText + f"&pageNo={current_page}&numOfRows={number_of_rows}"+ "&ServiceKey=" + client_key
        #print(url)

        hdr = {'Accept-Charset': 'utf-8'}
        request = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(request)

        if response.getcode() == 200: #정상
            res_dict = xmltodict.parse(response.read().decode('utf-8'))
            #print(res_dict)

            items = res_dict['response']['body']['items']['item']
            total_count = int(res_dict['response']['count']['totalCount']) #total_count 확인 가능
            for item in items:
                # yield 사용 
                yield extract_db_fields(item)
                # print(item)
        else: 
            print("Error Code", rescode)
            yield None #중단

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
        if keyword in item_in_db[0]:c

            print(f"{item['applicationNumber']} is not updated")
            return False #더이상 쿼리 안함
        else:
            new_keywords = item_in_db[0] + [keyword] #새로운 키워드를 집어둠
            cursor.execute(
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

# keyword와 연관된 특허를 crawling하여 DB에 저장
# Tuple 형태로 가지고 온다
def crawl_patents_into_db(keyword_in_db):
    # 화장료 키워드가 tuple 첫번쨰 꺼 위치하니까 [0]
    keyword = keyword_in_db[0]
    
    print('keyword', keyword)

    # yield에서 반횐된것
    # 하나씩 반환하여 후처리 함
    for item in crawl_patent_iterator(keyword):
        if item == None: #None은 예외적인 경우
            print(f"{keyword} 검색중에 문제가 발생하였습니다.")
            sys.exit(1) #error는 1
        #print("main", item)  
        
        # crawling 전처리 update 후처리
        updated = store_in_db(item, keyword)

        cursor.execute(
            '''UPDATE
                keywords_keyword
                SET updated=(%s)
                WHERE keyword=(%s)
            ''', datetime.datetime.now(), keyword)

        db.commit()

    # keywords_db_collection.update_one({'keyword': keyword}, {"$set": {"completed": True, "updated":datetime.datetime.now()}})
        


if __name__ == '__main__':
    # .env에 있는 환경변수 로드
    dotenv.load_dotenv(verbose=True)

    # 설정파일 불러오기
    conf = load_config_file()

    # DB 초기화
    db_user = os.getenv('DB_ROOT_USERNAME')
    db_password = os.getenv('DB_ROOT_PASSWORD')

    # DB Connect & Add cursor(DB 내용을 읽어오는 것) 
    db = psycopg2.connect(host='localhost', dbname='patents', port=5432, user=db_user, password=db_password)
    cursor = db.cursor()
    
    # 하루에 몇개를 crawling할 것인가(default 1)
    keywords_per_day = conf.get('keywords_per_day', 1)

    # Crawling할 갯수만큼 for문을 iteration
    for idx in range(0, keywords_per_day):
        # 가장 오래된 or 한번도 crawling하지 않은 것
        keyword = get_oldest_keyword(conf)
        print('Oldest Keyword', keyword)
        if keyword == None:
            print("No more keyword remained")
            sys.exit(0)
        
        crawl_patents_into_db(keyword)
