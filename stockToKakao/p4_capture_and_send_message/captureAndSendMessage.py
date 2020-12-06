import json
import requests
import traceback
import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule, messageModule, calcModule
from stockToKakao.p4_capture_and_send_message.bizLogic.decisionCaptureStock import decision_capture_stock


def main_process():
    # 시작시간
    start_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 헤더세팅
    headers = messageModule.set_headers()

    # 당일
    now_time = datetime.today().strftime("%Y%m%d%H%M%S")
    today = now_time[0:8]

    # 조회 기준일
    base_time = (datetime.today() - timedelta(days=14)).strftime("%Y%m%d%H%M%S")
    base_dt = base_time[0:8]

    # 제외 기준일
    except_time = (datetime.today() - timedelta(days=7)).strftime("%Y%m%d%H%M%S")
    except_dt = except_time[0:8]

    # DB 모듈선언
    db_class = dbModule.Database()

    # 당일 기 수행된 데이타가 있다면 clear
    sql = "DELETE from stock_search.stock_captured WHERE capture_tcd = '04' AND substring(capture_dttm, 1, 8) = '%s'" % today
    db_class.execute(sql)
    db_class.commit()

    # 대상건 조회
    # 14일 이내에 상승 가능성 예측된 종목 중에서 유통주식수 대비 거래량이 50% 이상인 것 추출
    # 그 중에서 7일 이내에 상승예상 종목 확인으로 알림 준것은 제외 한다.
    sql = "SELECT distinct a.stc_id, a.stc_name from stock_search.stock_basic a, stock_search.stock_captured b " \
          "where a.stc_id = b.stc_id and b.capture_tcd = '01' " \
          "and b.rate_of_quant > %d " \
          "AND substring(b.capture_dttm, 1, 8) >= '%s'" \
          "AND (a.stc_id, a.stc_name) NOT IN(" \
          "SELECT a.stc_id, a.stc_name from stock_search.stock_basic a, stock_search.stock_captured b " \
          "where a.stc_id = b.stc_id and b.capture_tcd = '04' " \
          "AND substring(b.capture_dttm, 1, 8) >= '%s')" % (20, base_dt, except_dt)
    rows = db_class.executeAll(sql)

    # 친구목록수신
    uuids = messageModule.get_friends(headers)

    # 친구 목록을 5개씩 나눔(카카오 한번에 최대 5명까지만 지원하므로)
    uuids_list = list(calcModule.divide_list(uuids, 5))
    print(uuids_list)
    # 조회된 건수 바탕으로 판별 및 송신
    for row in rows:
        try:
            # 판별대상 데이터
            stc_id = row['stc_id']
            stc_name = row['stc_name']

            # 판별 및 전송 (capture_stock 은 조건에 맞으면 종가를 리턴하고 조건에 안맞으면 0을 리턴한다.)
            price = decision_capture_stock(stc_id)
            if price > 0:

                # 데이터세팅 및 메시지 송신
                for friends in uuids_list:
                    # 데이터세팅
                    data = messageModule.set_data(stc_id, stc_name, '상승예상 종목확인!!', friends)

                    # 메시지송신
                    messageModule.send_message_to_friends(headers, data)

                # 결과저장
                sql = "insert into stock_search.stock_captured (capture_dttm, stc_id, price, capture_tcd, msg ) " \
                      "values('%s', '%s', '%d', '04', '%s')" % (now_time, stc_id, price, '상승예상 종목확인!!')
                db_class.execute(sql)
                db_class.commit()

        except Exception as ex:
            traceback.print_exc()

    # commit
    db_class.commit()

    # 종료 시간
    end_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 종료메시지
    print("급등임박 종목 메시지 송신 완료")
    print("시작시각: ", start_time)
    print("종료시각: ", end_time)


if __name__ == "__main__":
    main_process()
