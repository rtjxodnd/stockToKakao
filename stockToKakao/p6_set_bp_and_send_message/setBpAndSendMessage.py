import sys
import os
import logging
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule, messageModule
from stockToKakao.p6_set_bp_and_send_message.crawler.crawlStockNowPrice import getStockNowPrice
from stockToKakao.p6_set_bp_and_send_message.bizLogic.calBfNxResisPrice import cal_before_next_price
from stockToKakao.p6_set_bp_and_send_message.bizLogic.increaseYn import increase_yn

# 로거
logger = logging.getLogger(__name__)


# 작업모드 1번: 전고점 돌파시 메시지 송신
def sub_process_01():
    # DB 모듈선언
    db_class = dbModule.Database()

    # 메시지 헤더세팅
    headers = messageModule.set_headers()

    # 당일
    now_time = datetime.today().strftime("%Y%m%d%H%M%S")

    # 대상건 조회
    sql = "select a.stc_id, b.stc_name, a.now_price, a.before_price, a.next_price, b.resistance_price " \
          "from stock_search.stock_breakthrough a, stock_search.stock_basic b where a.stc_id = b.stc_id "
    rows = db_class.executeAll(sql)

    # 친구목록수신
    uuids = messageModule.get_friends(headers)

    # 조회된 건수 바탕으로 data 세팅 및 메시지 송신
    for row in rows:
        try:
            # 대상 데이터
            stc_id = row['stc_id']
            stc_name = row['stc_name']

            # 기존값
            before_price = int(row['before_price'])
            next_price = int(row['next_price'])
            resistance_price = row['resistance_price']

            # 현재가
            now_price = int(getStockNowPrice(stc_id)['now_price'])

            # 현재가가 이전 전고점보다 낮아졌거나 다음 전고점보다 높아진 경우
            # 전고점정보 확인 설정 및 DB 저장
            if now_price < before_price or now_price > next_price:

                # 전고점정보 확인 및 다음가격 설정
                new_price_value = cal_before_next_price(now_price, resistance_price)

                # DB저장
                sql = "update stock_search.stock_breakthrough " \
                      "set now_price = '%d', before_price= '%d', next_price= '%d'" \
                      "where stc_id = '%s'" % \
                      (now_price, new_price_value['before_price'], new_price_value['next_price'], stc_id)
                db_class.execute(sql)
                db_class.commit()

            # 현재가가 다음 전고점보다 높아졌으면서 거래량 및 가격 기준에 부합하는 경우
            # 메시지 송신
            if now_price > next_price and increase_yn(stc_id):
                # 데이터세팅
                data = messageModule.set_data(stc_id, stc_name, "전고점 돌파!!!", uuids)
                # 메시지송신
                messageModule.send_message_to_friends(headers, data)

                # 결과저장
                sql = "insert into stock_search.stock_captured (capture_dttm, stc_id, price, capture_tcd ) " \
                      "values('%s', '%s', '%d', '02')" % (now_time, stc_id, now_price)
                db_class.execute(sql)
                db_class.commit()

        except Exception as ex:
            logger.error("ERROR!!!!: sub_process_01")
            logger.error(ex)

    db_class.commit()
    print("전고점 돌파 메시지 송신 완료")
    return


# 작업모드 2번: 전고점 정보 및 현재가 가져오기
def sub_process_02():
    # DB 모듈선언
    db_class = dbModule.Database()

    # 데이타 clear
    sql = "DELETE from stock_search.stock_breakthrough"
    db_class.execute(sql)
    db_class.commit()

    # 대상건 조회
    sql = "SELECT stc_id, resistance_price " \
          "FROM stock_search.stock_basic " \
          "WHERE filter_cd = '01' AND resistance_price <> ''"
    rows = db_class.executeAll(sql)

    # 조회된 건수 바탕으로 data 세팅
    for row in rows:
        try:
            # 대상 데이터
            stc_id = row['stc_id']
            resistance_price = row['resistance_price']

            # 현재가
            now_price = int(getStockNowPrice(stc_id)['now_price'])

            # 전고점정보 확인 및 다음가격 설정
            new_price_value = cal_before_next_price(now_price, resistance_price)

            # DB저장
            sql = "insert into stock_search.stock_breakthrough (stc_id ,now_price, before_price, next_price) " \
                  "values( '%s','%d','%d','%d')" % \
                  (stc_id, now_price, new_price_value['before_price'], new_price_value['next_price'])
            db_class.execute(sql)
            db_class.commit()
        except Exception as ex:
            logger.error("ERROR!!!!: sub_process_02")
            logger.error(ex)

    db_class.commit()
    print("전고점 재설정 완료")
    return


def main_process():
    # 시작시간
    start_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 현재시간
    now_time = datetime.today().strftime("%H%M%S")

    # 시간대별 다른 프로세스 수행
    if '090000' <= now_time < '160000':
        sub_process_01()
    else:
        sub_process_02()

    # 종료 시간
    end_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 종료메시지
    print("저항선 돌파 종목 정보 송신 완료")
    print("시작시각: ", start_time)
    print("종료시각: ", end_time)


if __name__ == "__main__":
    main_process()
