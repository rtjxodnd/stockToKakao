import json
import requests
import logging
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule, messageModule
from stockToKakao.p4_capture_and_send_message.bizLogic.captureStock import capture_stock

# 로거
logger = logging.getLogger(__name__)


def main_process():
    # 시작시간
    start_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 헤더세팅
    headers = messageModule.set_headers()

    # 당일
    now_time = datetime.today().strftime("%Y%m%d%H%M%S")
    today = now_time[0:8]

    # DB 모듈선언
    db_class = dbModule.Database()

    # 당일 기 수행된 데이타가 있다면 clear
    sql = "DELETE from stock_search.stock_captured WHERE capture_tcd = '01'AND substring(capture_dttm, 1, 8) = '%s'" % today
    db_class.execute(sql)
    db_class.commit()

    # 대상건 조회
    sql = "SELECT stc_id, stc_name from stock_search.stock_basic where substring(bin(filter_bcd), -1, 1) = '1'"
    rows = db_class.executeAll(sql)

    # 친구목록수신
    uuids = messageModule.get_friends(headers)

    # 조회된 건수 바탕으로 판별 및 송신
    for row in rows:
        try:
            # 판별대상 데이터
            stc_id = row['stc_id']
            stc_name = row['stc_name']

            # 판별 및 전송 (capture_stock 은 조건에 맞으면 종가를 리턴하고 조건에 안맞으면 0을 리턴한다.)
            price = capture_stock(stc_id)
            if price > 0:

                # 데이터세팅
                data = messageModule.set_data(stc_id, stc_name, '상승예상 종목확인!!', uuids)

                # 결과저장
                sql = "insert into stock_search.stock_captured (capture_dttm, stc_id, price, capture_tcd, msg ) " \
                      "values('%s', '%s', '%d', '01', '%s')" % (now_time, stc_id, price, '상승예상 종목확인!!')
                db_class.execute(sql)
                db_class.commit()

                # 메시지송신
                messageModule.send_message_to_friends(headers, data)

        except Exception as ex:
            logger.error("ERROR!!!!: main_process")
            logger.error(ex)

    # commit
    db_class.commit()

    # 종료 시간
    end_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 종료메시지
    print("상승예상 종목 메시지 송신 완료")
    print("시작시각: ", start_time)
    print("종료시각: ", end_time)


if __name__ == "__main__":
    main_process()
