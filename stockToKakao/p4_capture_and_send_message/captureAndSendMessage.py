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
    # 헤더세팅
    headers = messageModule.set_headers()

    # 당일
    today = datetime.today().strftime("%Y%m%d")

    # DB 모듈선언
    db_class = dbModule.Database()

    # 당일 기 수행된 데이타가 있다면 clear
    sql = "DELETE from stock_search.stock_captured WHERE capture_tcd = '01'AND capture_dt = '%s'" % today
    db_class.execute(sql)
    db_class.commit()

    # 대상건 조회
    sql = "SELECT stc_id, stc_name from stock_search.stock_basic where filter_yn = 'Y'"
    rows = db_class.executeAll(sql)

    # 조회된 건수 바탕으로 판별 및 송신
    for row in rows:
        try:
            # 판별대상 데이터
            stc_id = row['stc_id']
            stc_name = row['stc_name']

            # 판별 및 전송
            if capture_stock(stc_id):

                # 데이터세팅
                data = messageModule.set_data(stc_id, stc_name, '상승예상 종목확인!!')

                # 결과저장
                sql = "insert into stock_search.stock_captured (capture_dt, stc_id ,capture_tcd ) " \
                      "values( '%s','%s','01')" % (today, stc_id)
                db_class.execute(sql)
                db_class.commit()

                # 메시지송신
                messageModule.send_message(headers, data)

        except Exception as ex:
            logger.error("ERROR!!!!: main_process")
            logger.error(ex)

    db_class.commit()
    print("상승예상 종목 메시지 송신 완료")


if __name__ == "__main__":
    main_process()
