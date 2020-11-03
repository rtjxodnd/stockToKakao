import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule
from stockToKakao.p3_get_filtered_stock_info.bizLogic.screen import main_process as screen
from stockToKakao.p3_get_filtered_stock_info.crawler.crawlImpairedRatio import find_impaired_ratio

# 로거
logger = logging.getLogger(__name__)


# DB 값 수정
def update_stock_info(db_class, stc_id):

    # 유통주식수 획득
    num_of_circulation = find_impaired_ratio(stc_id)['num_of_circulation']

    # DB Update
    try:
        sql = "UPDATE stock_search.stock_basic SET num_of_circulation = '%d', filter_yn = '%s'" \
              "WHERE stc_id = '%s'" % (num_of_circulation, 'Y', stc_id)
        db_class.execute(sql)
        db_class.commit()
        return
    except Exception as ex:
        error_result_dict = {"companyCode": stc_id}
        logger.error(error_result_dict)
        logger.error("ERROR!!!!: update_stock_info")
        logger.error(ex)


def main_process():
    # db 모듈선언
    db_class = dbModule.Database()

    # 초기화
    sql = "UPDATE stock_search.stock_basic SET filter_yn = 'N'"
    db_class.execute(sql)
    db_class.commit()

    # 대상건 조회

    sql = "SELECT stc_id, stc_name from stock_search.stock_basic " \
          "WHERE tot_value < 500000000000 and face_price > 0 " \
          "and substr(stc_name,-1) not in ('우', 'B', 'C') and stc_name not like '%%스팩%%'"
    rows = db_class.executeAll(sql)

    # 조회된 건수 바탕으로 판별 및 송신
    for i, row in enumerate(rows):
        try:
            if i % 10 == 0:
                print("판단중.... 전체:", len(rows), "건, 현재: ", i, "건")

            # 판별대상 데이터
            stc_id = row['stc_id']

            # 판별 및 DB 값 수정
            if screen(stc_id):

                # db 값 변경
                update_stock_info(db_class, stc_id)

        except Exception as ex:
            logger.error("ERROR!!!!: main_process")
            logger.error(ex)

    # 종료 메시지
    db_class.commit()
    print("재무 가격 정보 판단완료!!!!")


if __name__ == "__main__":
    main_process()
