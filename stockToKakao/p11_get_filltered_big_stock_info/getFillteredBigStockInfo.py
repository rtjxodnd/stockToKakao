import logging
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule
from stockToKakao.p11_get_filltered_big_stock_info.bizLogic.screen import main_process as screen
from stockToKakao.p11_get_filltered_big_stock_info.crawler.crawlImpairedRatio import find_impaired_ratio


# 로거
logger = logging.getLogger(__name__)


# DB 값 수정(재무정보)
def update_stock_fin_info(db_class, stc_id):

    # 유통주식수 획득
    num_of_circulation = find_impaired_ratio(stc_id)['num_of_circulation']

    # DB Update
    try:
        sql = "UPDATE stock_search.stock_basic SET num_of_circulation = '%d', filter_bcd = filter_bcd | b'%s'" \
              "WHERE stc_id = '%s'" % (num_of_circulation, '010', stc_id)
        db_class.execute(sql)
        db_class.commit()
        return
    except Exception as ex:
        error_result_dict = {"companyCode": stc_id}
        logger.error(error_result_dict)
        logger.error("ERROR!!!!: update_stock_fin_info")
        logger.error(ex)


def main_process(input_stc_id = None):
    # 시작시간
    start_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # db 모듈선언
    db_class = dbModule.Database()

    # 대상건 조회(우선주/스펙주제외)
    sql = "SELECT stc_id, stc_name from stock_search.stock_basic " \
          "WHERE tot_value > 500000000000 and face_price > 0 " \
          "and preferred_stc_yn = 'N' " \
          "and stc_name not like '%%스팩%%'"

    # 특정종목번호 들어온 경우는 이를 수행
    if input_stc_id is not None:
        sql = "SELECT stc_id, stc_name from stock_search.stock_basic " \
              "WHERE stc_id = '%s'" % input_stc_id

    rows = db_class.executeAll(sql)

    # 조회된 건수 바탕으로 판별 및 송신
    for i, row in enumerate(rows):
        try:
            if i % 10 == 0:
                print("판단중(우선주/스펙주제외).... 전체:", len(rows), "건, 현재: ", i, "건")

            # 판별대상 데이터
            stc_id = row['stc_id']

            # 판별 및 DB 값 수정
            if screen(stc_id):

                # db 값 변경
                update_stock_fin_info(db_class, stc_id)

        except Exception as ex:
            error_result_dict = {"companyCode": stc_id}
            logger.error(error_result_dict)
            logger.error("ERROR!!!!: main_process")
            logger.error(ex)

    # commit
    db_class.commit()

    # 종료 시간
    end_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 최종 종료메시지
    print("시작시각: ", start_time)
    print("종료시각: ", end_time)


if __name__ == "__main__":
    main_process()

