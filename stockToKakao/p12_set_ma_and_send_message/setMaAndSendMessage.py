import sys
import os
import traceback
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule, messageModule, calcModule
from stockToKakao.p12_set_ma_and_send_message.bizLogic.cal_move_avg_values import cal_move_avg_values


# 작업모드 1번: 이평선 돌파시 메시지 송신
def sub_process_01(in_stc_id=None):
    # DB 모듈선언
    db_class = dbModule.Database()

    # 메시지 헤더세팅
    headers = messageModule.set_headers()

    # 당일
    now_time = datetime.today().strftime("%Y%m%d%H%M%S")

    # 대상건 조회
    sql = "select a.stc_id, b.stc_name, a.now_price, a.ma5, a.ma20, a.ma60, a.ma120, a.ma240 " \
          "from stock_search.stock_move_avg a, stock_search.stock_basic b where a.stc_id = b.stc_id "

    if in_stc_id is not None:
        sql = "select a.stc_id, b.stc_name, a.now_price, a.ma5, a.ma20, a.ma60, a.ma120, a.ma240 " \
              "from stock_search.stock_move_avg a, stock_search.stock_basic b " \
              "where a.stc_id = b.stc_id and a.stc_id = '%s'" % in_stc_id

    rows = db_class.executeAll(sql)

    # 친구목록수신
    uuids = messageModule.get_friends(headers)

    # 친구 목록을 5개씩 나눔(카카오 한번에 최대 5명까지만 지원하므로)
    uuids_list = list(calcModule.divide_list(uuids, 5))

    # 조회된 건수 바탕으로 data 세팅 및 메시지 송신
    for row in rows:
        try:
            # 대상 데이터
            stc_id = row['stc_id']
            stc_name = row['stc_name']

            # 기존값
            old_now_price = row['now_price']
            old_ma5 = row['ma5']
            old_ma20 = row['ma20']
            old_ma60 = row['ma60']
            old_ma120 = row['ma120']
            old_ma240 = row['ma240']

            # 현재가 및 이동평균가격
            price_info = cal_move_avg_values(stc_id)
            now_price = price_info['now_price']
            ma5 = price_info['ma5']
            ma20 = price_info['ma20']
            ma60 = price_info['ma60']
            ma120 = price_info['ma120']
            ma240 = price_info['ma240']

            # 새로운 값 DB저장
            sql = "update stock_search.stock_move_avg " \
                  "set now_price = '%d', ma5 = '%d', ma20 = '%d', ma60= '%d', ma120 = '%d', ma240 = '%d'" \
                  "where stc_id = '%s'" % (now_price, ma5, ma20, ma60, ma120, ma240, stc_id)
            db_class.execute(sql)
            db_class.commit()

            # 메시지조합
            yn_now = False
            yn_5 = False
            yn_20 = False
            yn_60 = False
            yn_120 = False

            msg_temp = ""
            msg_now = ""
            msg_5 = ""
            msg_20 = ""
            msg_60 = ""
            msg_120 = ""

            # 현재가 5일선돌파
            if old_now_price <= old_ma5 and now_price > ma5:
                msg_temp = msg_temp+"5 "
                yn_now = True

            # 현재가 20일선돌파
            if old_now_price <= old_ma20 and now_price > ma20:
                msg_temp = msg_temp+"20 "
                yn_now = True

            # 현재가 60일선돌파
            if old_now_price <= old_ma60 and now_price > ma60:
                msg_temp = msg_temp+"60 "
                yn_now = True

            # 현재가 120일선돌파
            if old_now_price <= old_ma120 and now_price > ma120:
                msg_temp = msg_temp+"120 "
                yn_now = True

            # 현재가 240일선돌파
            if old_now_price <= old_ma240 and now_price > ma240:
                msg_temp = msg_temp+"240 "
                yn_now = True

            # 메시지 조립
            if yn_now:
                msg_now = "현재가: " + msg_temp + "일선 돌파! \n"
            msg_temp = ""

            # 5일선 20일선돌파
            if old_ma5 <= old_ma20 and ma5 > ma20:
                msg_temp = msg_temp+"20 "
                yn_5 = True

            # 5일선 60일선돌파
            if old_ma5 <= old_ma60 and ma5 > ma60:
                msg_temp = msg_temp+"60 "
                yn_5 = True

            # 5일선 120일선돌파
            if old_ma5 <= old_ma120 and ma5 > ma120:
                msg_temp = msg_temp+"120 "
                yn_5 = True

            # 5일선 240일선돌파
            if old_ma5 <= old_ma240 and ma5 > ma240:
                msg_temp = msg_temp+"240 "
                yn_5 = True

            # 메시지 조립
            if yn_5:
                msg_5 = "5일선: " + msg_temp + "일선 돌파! \n"
            msg_temp = ""

            # # 20일선 60일선돌파
            # if old_ma20 <= old_ma60 and ma20 > ma60:
            #     msg_temp = msg_temp+"60 "
            #     yn_20 = True

            # 20일선 120일선돌파
            if old_ma20 <= old_ma120 and ma20 > ma120:
                msg_temp = msg_temp+"120 "
                yn_20 = True

            # # 20일선 240일선돌파
            # if old_ma20 <= old_ma240 and ma20 > ma240:
            #     msg_temp = msg_temp+"240 "
            #     yn_20 = True

            # 메시지 조립
            if yn_20:
                msg_20 = "20일선: " + msg_temp + "일선 돌파! \n"
            msg_temp = ""

            # 60일선 120일선돌파
            if old_ma60 <= old_ma120 and ma60 > ma120:
                msg_temp = msg_temp+"120 "
                yn_60 = True

            # 60일선 240일선돌파
            if old_ma60 <= old_ma240 and ma60 > ma240:
                msg_temp = msg_temp+"240 "
                yn_60 = True

            # 메시지 조립
            if yn_60:
                msg_60 = "60일선: " + msg_temp + "일선 돌파! \n"
            msg_temp = ""

            # 120일선 240일선돌파
            if old_ma120 <= old_ma240 and ma120 > ma240:
                msg_temp = msg_temp+"240 "
                yn_120 = True

            # 메시지 조립
            if yn_120:
                msg_120 = "120일선: " + msg_temp + "일선 돌파! \n"

            # 최종 메시지 조립
            msg_final = msg_now+msg_5+msg_20+msg_60+msg_120
            msg_final = msg_20

            # 메시지 송신
            # if yn_now or yn_5 or yn_20 or yn_60 or yn_120:
            if yn_20:
                # 데이터세팅 및 메시지송신
                for friends in uuids_list:
                    # 데이터세팅
                    data = messageModule.set_data(stc_id, stc_name, msg_final, friends)
                    # 메시지송신
                    messageModule.send_message_to_friends(headers, data)

                # 결과저장
                sql = "insert into stock_search.stock_captured (capture_dttm, stc_id, price, capture_tcd, msg ) " \
                      "values('%s', '%s', '%d', '03', '%s')" % (now_time, stc_id, now_price, msg_final)
                db_class.execute(sql)
                db_class.commit()

        except Exception as ex:
            traceback.print_exc()

    db_class.commit()
    print("이평선 돌파 메시지 송신 완료")
    return


# 작업모드 2번: 이평선 정보 및 현재가 가져오기
def sub_process_02(in_stc_id=None):
    # DB 모듈선언
    db_class = dbModule.Database()

    # 데이타 clear
    sql = "DELETE from stock_search.stock_move_avg"
    db_class.execute(sql)
    db_class.commit()

    # 대상건 조회
    sql = "SELECT stc_id " \
          "FROM stock_search.stock_basic " \
          "WHERE substring(bin(filter_bcd), -2, 1) = '1'"
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

    # 현재시간
    now_time = datetime.today().strftime("%H%M%S")

    # 시간대별 다른 프로세스 수행
    if '090000' <= now_time < '160000':
        sub_process_01(in_stc_id)
    else:
        sub_process_02(in_stc_id)

    # 종료 시간
    end_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 종료메시지
    print("시작시각: ", start_time)
    print("종료시각: ", end_time)


if __name__ == "__main__":
    main_process()
