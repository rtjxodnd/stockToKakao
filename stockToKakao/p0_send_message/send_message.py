import logging
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import messageModule, calcModule

# 로거
logger = logging.getLogger(__name__)


def main_process():
    # 시작시간
    start_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 헤더세팅
    headers = messageModule.set_headers()

    # 당일
    now_time = datetime.today().strftime("%Y%m%d%H%M%S")

    # 친구목록수신
    uuids = messageModule.get_friends(headers)

    # 친구 목록을 5개씩 나눔(카카오 한번에 최대 5명까지만 지원하므로)
    uuids_list = list(calcModule.divide_list(uuids, 5))

    # 메시지 송신
    try:
        # 판별대상 데이터
        stc_id = '005930'
        stc_name = '테스트_삼성전자'

        # for friends in uuids_list:
        #     # 데이터세팅
        #     data = messageModule.set_data(stc_id, stc_name, '메시지송신 테스트입니다.', friends)
        #
        #     # 메시지송신
        #     messageModule.send_message_to_friends(headers, data)

    except Exception as ex:
        logger.error("ERROR!!!!: main_process")
        logger.error(ex)

    # 종료 시간
    end_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 종료메시지
    print("상승예상 종목 메시지 송신 완료")
    print("시작시각: ", start_time)
    print("종료시각: ", end_time)


if __name__ == "__main__":
    main_process()
