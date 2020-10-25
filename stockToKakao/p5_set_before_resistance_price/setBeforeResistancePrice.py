import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule
from stockToKakao.p5_set_before_resistance_price.crawler.crawlDailyStockPriceInfo import main_process as crawlPrice
from stockToKakao.p5_set_before_resistance_price.bizLogic.calbfResisPrice import cal_before_resistance_price as cbrp
from stockToKakao.commonModule.calcModule import listToString

def main_process(term):

    # 당일
    today = datetime.today().strftime("%Y%m%d")

    # DB 모듈선언
    db_class = dbModule.Database()

    # 대상건 조회
    sql = "SELECT stc_id, stc_dvsn, now_price from stock_search.stock_basic where filter_yn = 'Y'"
    # sql = "SELECT stc_id, stc_dvsn, now_price from stock_search.stock_basic where stc_id = '289010'"
    rows = db_class.executeAll(sql)

    # 조회된 건수 바탕으로 전고점 추출
    for i, row in enumerate(rows):
        # 대상 데이터
        stc_id = row['stc_id']
        stc_dvsn = row['stc_dvsn']
        now_price = row['now_price']

        # 과거 시가, 종가 추출
        priceList = crawlPrice(stc_id, term)

        # 가격정보중 고가/저가만 추출하여 저장
        extractList = []
        for priceInfo in priceList:
            extractList.append(int(priceInfo['hig_price']))
            extractList.append(int(priceInfo['low_price']))

        # 전고점 계산
        before_resistance_price = cbrp(stc_dvsn, now_price, extractList)
        before_resistance_price_str = listToString(before_resistance_price)
        # print(before_resistance_price_str)
        # 결과저장
        sql = "UPDATE stock_search.stock_basic set before_resistance_price = '%s' where stc_id = '%s'" \
              % (before_resistance_price_str, stc_id)
        db_class.execute(sql)
        db_class.commit()

        # 진행상황
        if i % 10 == 0:
            print("총 %d건 중 %d건 완료" % (len(rows), i))

    print("\n전고점 설정 완료")


if __name__ == "__main__":
    main_process(12)
