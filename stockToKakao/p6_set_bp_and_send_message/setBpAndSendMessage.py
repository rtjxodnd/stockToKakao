import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule, messageModule, timeModule
from stockToKakao.p6_set_bp_and_send_message.crawler.crawlStockNowPrice import getStockNowPrice
from stockToKakao.p6_set_bp_and_send_message.bizLogic.calBfNxResisPrice import cal_before_next_price
from stockToKakao.p6_set_bp_and_send_message.bizLogic.increaseYn import increase_yn


# 작업모드 1번: 전고점 돌파시 메시지 송신
def sub_process_01():
    # DB 모듈선언
    db_class = dbModule.Database()

    # 메시지 헤더세팅
    headers = messageModule.set_headers()

    # 대상건 조회
    sql = "select a.stc_id, b.stc_name, a.now_price, a.before_price, a.next_price, b.resistance_price " \
          "from stock_search.stock_breakthrough a, stock_search.stock_basic b where a.stc_id = b.stc_id "
    rows = db_class.executeAll(sql)

    # 조회된 건수 바탕으로 data 세팅 및 메시지 송신
    for row in rows:
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
            data = messageModule.set_data(stc_id, stc_name, "전고점 돌파!!!")
            # 메시지송신
            messageModule.send_message(headers, data)

    print("\n메시지 송신 완료")
    db_class.commit()
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
          "WHERE filter_yn = 'Y' AND resistance_price <> ''"
    rows = db_class.executeAll(sql)

    # 조회된 건수 바탕으로 data 세팅
    for row in rows:
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

    print("\n전고점 설정 완료")
    db_class.commit()
    return


def main_process():
    # 현재시간
    nowTime = timeModule.get_server_time()

    # 시간대별 다른 프로세스 수행
    if '090000' <= nowTime < '160000':
        sub_process_01()
    else:
        sub_process_02()


if __name__ == "__main__":
    main_process()
