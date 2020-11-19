# 필요라이브러리 import
import logging
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule
from stockToKakao.p2_get_stock_basic_info.crawler.crawlOnePageValues import crawl_one_page_values


# 로거
logger = logging.getLogger(__name__)


# 한건의 data 추출
def find_one_stock_values(sosok, page, stockOrder, tr):
    tds = tr.find_all("td")

    # 주식구분 설정
    if sosok == 0:
        stc_dvsn = "01"
    elif sosok == 1:
        stc_dvsn = "02"
    else:
        stc_dvsn = "03"

    # 필요 데이터 추출
    result_value = {"endOfData": "N",
                    "sosok": sosok,
                    "page": page,
                    "stockOrder": stockOrder,
                    "stcId": tds[1].find("a").get('href')[-6:],  # 종목코드
                    "stcNm": tds[1].find("a").text,  # 종목명
                    "stcDvsn": stc_dvsn,
                    "nowPrice": float(tds[2].text.replace(",", "")),  # 현재가
                    "facePrice": float(tds[5].text.replace(",", "")),  # 액면가
                    "totValue": float(tds[6].text.replace(",", "")) * 100000000,  # 시가총액
                    "dealAmt": float(tds[9].text.replace(",", "")) * float(tds[2].text.replace(",", ""))}  # 거래금액

    # db 입력
    stock_values_insert_to_db(result_value)

    return result_value


# 한페이지의 data 추출
# sosok: 0코스닥, 1코스피
# page: 웹 페이지 지정
# stockOrder: 해당 페이지 내에서의 순서
def find_one_page_values(sosok=0, page=1):
    try:
        # 데이터 탐색
        one_page_values = crawl_one_page_values(sosok, page)

        # 한페이지 내의 각 종목 정보 추출/저장
        for stockOrder in range(0, 50):
            one_stock_values = one_page_values[stockOrder]
            result_value = find_one_stock_values(sosok, page, stockOrder, one_stock_values)

        return result_value

    except IndexError:
        # 페이지의 끝
        result_value = {"endOfData": "Y",
                        "sosok": sosok,
                        "page": page,
                        "stockOrder": stockOrder}

        # return
        return result_value

    except Exception as ex:
        logger.error("ERROR!!!!: find_one_page_values")
        logger.error(ex)


# 기존 data delete
def stock_values_delete():

    try:
        db_class = dbModule.Database()
        sql = "DELETE from stock_search.stock_basic"
        db_class.execute(sql)
        db_class.commit()

        return
    except Exception as ex:
        logger.error("ERROR!!!!: stock_values_delete")
        logger.error(ex)


# 입력된 dictionary 를 db insert
# insert_value: 입력된 dictionary 형태의 종목정보
def stock_values_insert_to_db(insert_value):
    stc_id = insert_value['stcId']
    stc_name = insert_value['stcNm']
    stc_dvsn = insert_value['stcDvsn']
    now_price = insert_value['nowPrice']
    face_price = insert_value['facePrice']
    tot_value = insert_value['totValue']
    deal_amt = insert_value['dealAmt']

    try:
        db_class = dbModule.Database()
        sql = "INSERT INTO stock_search.stock_basic(" \
              "stc_id, " \
              "stc_name, " \
              "stc_dvsn, " \
              "now_price, " \
              "face_price, " \
              "tot_value, " \
              "deal_amt, " \
              "filter_bcd) " \
              "VALUES('%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d')" % \
              (stc_id, stc_name, stc_dvsn,
               now_price, face_price, tot_value, deal_amt, 0)
        db_class.execute(sql)
        db_class.commit()
        return
    except Exception as ex:
        error_result_dict = { "companyCode": insert_value['stcId']
                            , "sosok": insert_value['sosok']
                            , "page": insert_value['page']
                            , "stockOrder": insert_value['stockOrder']}
        logger.error(error_result_dict)
        logger.error("ERROR!!!!: stock_values_insert_to_db")
        logger.error(ex)


# 우선주여부 update
def preferred_stock_values_update():

    try:
        db_class = dbModule.Database()
        sql = "UPDATE stock_search.stock_basic set preferred_stc_yn = 'Y'" \
              "WHERE substr(stc_name,-1) in ('우', 'B', 'C')" \
              "and stc_name like '%우%'" \
              "and stc_name not in ('미래에셋대우', '연우', '나우IB', '이오플로우')"
        db_class.execute(sql)
        db_class.commit()

        return
    except Exception as ex:
        logger.error("ERROR!!!!: preferred_stock_values_update")
        logger.error(ex)


###########################################################
# Main 처리: 주식 기본 테이블삭제 후 data 읽어서 주식기본 테이블에 저장한다.
###########################################################
def main_process():
    # 시작시간
    start_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 기존자료 삭제
    stock_values_delete()

    # 코스피(소속=0, 전체 페이지=31)
    sosok = 0
    tot_pages = 32 + 1

    for page in range(1, tot_pages):
        try:
            # 한페이지의 data 추출
            if find_one_page_values(sosok, page)['endOfData'] == 'Y':
                logger.error("kospi data 끝")
                break
        except Exception as ex:
            logger.error("ERROR!!!!: main_process")
            logger.error(ex)

    # 코스닥(소속=1, 전체 페이지=28)
    sosok = 1
    tot_pages = 29 + 1

    for page in range(1, tot_pages):
        try:
            # 한페이지의 data 추출
            if find_one_page_values(sosok, page)['endOfData'] == 'Y':
                logger.error("kosdaq data 끝")
                break
        except Exception as ex:
            logger.error("ERROR!!!!: main_process")
            logger.error(ex)

    # 우선주여부 update
    preferred_stock_values_update()

    # 종료 시간
    end_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 종료메시지
    print("종목정보 수신종료!!!")
    print("시작시각: ", start_time)
    print("종료시각: ", end_time)


if __name__ == "__main__":
    main_process()

