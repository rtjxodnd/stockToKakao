import json
import requests
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule, ipModule
from stockToKakao.p6_set_bp_and_send_message.crawler.crawlStockNowPrice import getStockNowPrice


# 헤더세팅
def set_headers():
    # 토큰조회
    db_class = dbModule.Database()
    sql = "SELECT access_token from stock_search.kakao_token"
    row = db_class.executeOne(sql)

    # 헤더세팅
    headers = {
        "Authorization": "Bearer " + row['access_token']
    }
    return headers


# 데이터세팅
def set_data(stc_id, stc_name):
    data = {
        "template_object": json.dumps({"object_type": "text",
                                       "text": "전고점 돌파!!\n "
                                               "["+stc_name+"]\n"
                                               " https://finance.naver.com/item/main.nhn?code="+stc_id,
                                       "link": {
                                           "web_url": "https://www.daum.com/",
                                           "mobile_web_url": "https://www.daum.com/"},
                                       "button_title": "네이버증권 바로가기"
                                       })}
    print('\n송신대상: '+stc_id+"["+stc_name+"]")
    return data


# 메시지송신
def send_message(headers, data):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    response = requests.post(url, headers=headers, data=data)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))


def select_work_mode():
    ip_name = ipModule.get_ip()['ip_name']
    time = datetime.today().strftime("%H%M%S")
    workMode = ""

    if ip_name == 'awsServer':
        if time >= '000000' and time < '070000':
            workMode = '1'
        else:
            workMode = '2'
    elif ip_name == 'localServer':
        if time >= '090000' and time < '160000':
            workMode = '1'
        else:
            workMode = '2'

    return workMode


def main_process():
    # # 헤더세팅
    # headers = set_headers()

    # 당일
    today = datetime.today().strftime("%Y%m%d")
    time = datetime.today().strftime("%H%M%S")

    print(today, time, select_work_mode())
    # # DB 모듈선언
    # db_class = dbModule.Database()
    #
    # # 당일 기 수행된 데이타가 있다면 clear
    # sql = "DELETE from stock_search.stock_captured WHERE capture_tcd = '01'AND capture_dt = '%s'" % today
    # db_class.execute(sql)
    # db_class.commit()
    #
    # # 대상건 조회
    # sql = "SELECT stc_id, stc_name from stock_search.stock_basic where filter_yn = 'Y'"
    # rows = db_class.executeAll(sql)
    #
    # # 조회된 건수 바탕으로 판별 및 송신
    # for row in rows:
    #     # 판별대상 데이터
    #     stc_id = row['stc_id']
    #     stc_name = row['stc_name']
    #
    #     # 판별 및 전송
    #     if capture_stock(stc_id):
    #
    #         # 데이터세팅
    #         data = set_data(stc_id, stc_name)
    #
    #         # 결과저장
    #         sql = "insert into stock_search.stock_captured (capture_dt, stc_id ,capture_tcd ) " \
    #               "values( '%s','%s','01')" % (today, stc_id)
    #         db_class.execute(sql)
    #         db_class.commit()
    #
    #         # 메시지송신
    #         send_message(headers, data)
    #
    # print("\n메시지 송신 완료")


if __name__ == "__main__":
    main_process()
