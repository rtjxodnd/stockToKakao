import sys
import os
import logging
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule, calcModule
from stockToKakao.p5_set_resistance_price.crawler.crawlDailyStockPriceInfo import main_process as crawlPrice
from stockToKakao.p5_set_resistance_price.bizLogic.calResisPrice import cal_resistance_price as crp
from stockToKakao.commonModule.calcModule import listToString

# 로거
logger = logging.getLogger(__name__)


def main_process(term):
    # 시작시간
    start_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # DB 모듈선언
    db_class = dbModule.Database()

    # 대상건 조회
    sql = "SELECT stc_id, stc_dvsn, now_price " \
          "from stock_search.stock_basic " \
          "where substring(bin(filter_bcd), -1, 1) = '1'"
    # sql = "SELECT stc_id, stc_dvsn, now_price from stock_search.stock_basic where stc_id = '005930'"
    rows = db_class.executeAll(sql)

    # 조회된 건수 바탕으로 전고점 추출
    for i, row in enumerate(rows):
        try:
            # 대상 데이터
            stc_id = row['stc_id']
            stc_dvsn = row['stc_dvsn']
            now_price = row['now_price']

            # 과거 고가, 저가 추출
            priceList = crawlPrice(stc_id, term)

            # 가격정보중 고가/저가만 추출하여 저장
            extractList = []
            for priceInfo in priceList:
                extractList.append(int(priceInfo['hig_price']))
                extractList.append(int(priceInfo['low_price']))

            # 전고점 계산
            resistance_price = crp(stc_dvsn, now_price, extractList)
            resistance_price_str = listToString(resistance_price)

            # 과거 종가 추출(3개월)
            priceList = crawlPrice(stc_id, 3)

            # 가격정보중 종가만 추출하여 저장
            extractList = []
            for priceInfo in priceList:
                extractList.append(int(priceInfo['cls_price']))

            # 변이계수 계산
            cv = calcModule.coefficient_of_variation(extractList)['cv']


            # 결과저장
            sql = "UPDATE stock_search.stock_basic " \
                  "set resistance_price = '%s' , coef_variation = '%f'" \
                  "where stc_id = '%s'" \
                  % (resistance_price_str, cv, stc_id)
            db_class.execute(sql)
            db_class.commit()

            # 진행상황
            if i % 10 == 0:
                print("총 %d건 중 %d건 완료" % (len(rows), i))
        except Exception as ex:
            logger.error("ERROR!!!!: main_process")
            logger.error(ex)

    # commit
    db_class.commit()

    # 종료 시간
    end_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 종료메시지
    print("지지선 저항선 설정 완료")
    print("시작시각: ", start_time)
    print("종료시각: ", end_time)


if __name__ == "__main__":
    main_process(12)
