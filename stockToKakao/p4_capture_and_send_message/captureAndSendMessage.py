import json
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule
from stockToKakao.p4_capture_and_send_message.bizLogic.captureStock import capture_stock


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
                                       "text": "상승예상 종목확인!!\n "
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


def main_process():
    # 헤더세팅
    headers = set_headers()

    # 대상건 조회
    db_class = dbModule.Database()
    sql = "SELECT stc_id, stc_name from stock_search.stock_basic where filter_yn = 'Y'"
    rows = db_class.executeAll(sql)

    # 조회된 건수 바탕으로 판별 및 송신
    for row in rows:
        # 판별대상 데이터
        stc_id = row['stc_id']
        stc_name = row['stc_name']

        # 판별 및 전송
        if capture_stock(stc_id):

            # 데이터세팅
            data = set_data(stc_id, stc_name)

            # 메시지송신
            send_message(headers, data)

    print("메시지 송신 완료")


if __name__ == "__main__":
    main_process()
