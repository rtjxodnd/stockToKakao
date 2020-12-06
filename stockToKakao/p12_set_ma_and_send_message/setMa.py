import sys
import os
import traceback
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule
from stockToKakao.p12_set_ma_and_send_message.bizLogic.cal_move_avg_values import cal_move_avg_values


# 이평선 정보 및 현재가 가져오기
def set_ma(in_stc_id=None):
    # DB 모듈선언
    db_class = dbModule.Database()

    # 데이타 clear
    sql = "DELETE from stock_search.stock_move_avg"
    db_class.execute(sql)
    db_class.commit()

    # 대상건 조회
    sql = "SELECT stc_id " \
          "FROM stock_search.stock_basic "
    if in_stc_id is not None:
        sql = "SELECT stc_id FROM stock_search.stock_basic WHERE stc_id = '%s'" % in_stc_id

    rows = db_class.executeAll(sql)

    # 조회된 건수 바탕으로 data 세팅
    for i, row in enumerate(rows):
        try:
            if i % 10 == 0:
                print("이평선정보 계산중.... 전체:", len(rows), "건, 현재: ", i, "건")

            # 대상 데이터
            stc_id = row['stc_id']

            # 현재가 및 이동평균가격
            price_info = cal_move_avg_values(stc_id)
            now_price = price_info['now_price']
            ma5 = price_info['ma5']
            ma20 = price_info['ma20']
            ma60 = price_info['ma60']
            ma120 = price_info['ma120']
            ma240 = price_info['ma240']

            # 이평선정보 저장
            sql = "insert into stock_search.stock_move_avg (stc_id ,now_price, ma5, ma20, ma60, ma120, ma240) " \
                  "values( '%s','%d','%d','%d','%d','%d','%d')" % (stc_id, now_price, ma5, ma20, ma60, ma120, ma240)
            db_class.execute(sql)
            db_class.commit()
        except Exception as ex:
            traceback.print_exc()

    db_class.commit()
    print("이평선정보 재설정 완료")
    return


def main_process(in_stc_id=None):
    # 시작시간
    start_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 프로세스 수행
    set_ma(in_stc_id)

    # 종료 시간
    end_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 종료메시지
    print("시작시각: ", start_time)
    print("종료시각: ", end_time)


if __name__ == "__main__":
    main_process()
