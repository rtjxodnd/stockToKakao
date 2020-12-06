import json
import requests
import traceback
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule, messageModule, calcModule
from stockToKakao.p4_capture_and_send_message.bizLogic.decisionPossibleStock import decision_possible_stock


def main_process():
    # 시작시간
    start_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

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
    sql = "SELECT stc_id, stc_name, num_of_circulation from stock_search.stock_basic where substring(bin(filter_bcd), -1, 1) = '1'"
    rows = db_class.executeAll(sql)

    # 조회된 건수 바탕으로 판별 및 송신
    for row in rows:
        try:
            # 판별대상 데이터
            stc_id = row['stc_id']

            # 판별 및 전송 (decision_possible_stock 은 조건에 맞으면 종가를 리턴하고 조건에 안맞으면 0을 리턴한다.)
            deal_info = decision_possible_stock(stc_id)
            price = float(deal_info['cls_price'])
            deal_qnt = deal_info['dealQnt']
            roq = round((deal_qnt / float(row['num_of_circulation'])) * 100, 2)

            if price > 0:
                # 결과저장
                sql = "insert into stock_search.stock_captured (capture_dttm, stc_id, price, rate_of_quant, capture_tcd, msg ) " \
                      "values('%s', '%s', '%d', '%d', '01', '%s')" % (now_time, stc_id, price, roq, '상승가능성 종목확인!!')
                db_class.execute(sql)
                db_class.commit()

        except Exception as ex:
            traceback.print_exc()

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
