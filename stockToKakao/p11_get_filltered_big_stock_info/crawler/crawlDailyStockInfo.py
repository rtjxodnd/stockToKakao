# https://finance.naver.com 으로부터 일별 종가정보를 크롤링한다.

# 필요라이브러리 import
import requests
from bs4 import BeautifulSoup
import logging


# 공통변수
FINANCE_URL = "https://finance.naver.com/item/sise_day.nhn?code="


# 해당 종목의 3년전 page 추출
def get_last_page_of_stock(stc_id):
    # 로거
    logger = logging.getLogger(__name__)

    try:
        url = FINANCE_URL+stc_id
        page_call_result = requests.get(url)
        bs_obj = BeautifulSoup(page_call_result.content, "html.parser")
        td_pg_rr = bs_obj.find("td", {"class": "pgRR"})

        # 마지막 페이지가 가리키는 위치 확인
        # 마지막 페이지 링크버튼 없다면 해당 종목은 1개의 페이지만 존재한다.
        if td_pg_rr is None:
            last_page = 1
        else:
            href = td_pg_rr.find("a")["href"]
            last_page = int(href.split("=")[2])

        # 대략 3년전 : 74 page, 그 이후 데이터만 확인
        if last_page > 74:
            last_page = 74

        return last_page
    except Exception as ex:
        logger.error("ERROR!!!!: get_last_page_of_stock")
        logger.error(ex)


# 한건의 data 추출
# tds: 입력된 tds data
# stockOrder: 해당 페이지 내에서의 순서
def find_stock_values_of_one(tds):

    # 필요 데이터 추출
    base_dt = tds[0].find("span").text.replace(".", "")  # 기준일
    cls_price = tds[1].find("span").text.replace(",", "")  # 금일종가
    deal_qnt = tds[6].text.replace(",", "")  # 거래량
    deal_amt = float(cls_price) * float(deal_qnt)  # 거래량
    over10billioYn = "N"

    # 거래금액 판별
    if deal_amt >= 10000000000:
        over10billioYn = "Y"

    # 결과세팅
    result_value = {"over10billioYn": over10billioYn, "baseDt": base_dt, "dealAmt": deal_amt}

    # return
    return result_value


# 한개 page 처리
def find_stock_values_of_one_page(stock_id, page=1):
    # 로거
    logger = logging.getLogger(__name__)

    try:
        # 데이터 탐색
        url = FINANCE_URL+stock_id+"&page="+str(page)
        page_call_result = requests.get(url)
        bs_obj = BeautifulSoup(page_call_result.content, "html.parser")
        # driver = set_page_driver(url)
        # bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
        # driver.close()

        trs = bs_obj.find_all("tr", {"onmouseover": "mouseOver(this)"})

        # 해당 page 의 last order 구하기(보통 한페이지당 10개의 일자 데이터가 있다. 그러나 마지막 데이터는 그보다 적음)
        last_order = -1
        for order in range(0, 10):
            tr = trs[order]
            tds = tr.find_all("td", {"align": "center"})
            if len(tds[0].text.replace(".", "").replace(" ", "")) == 0:
                break
            last_order = last_order + 1

        # 필요 데이터 추출
        for order in range(0, last_order):
            tr = trs[order]
            tds = tr.find_all("td")
            result_value = find_stock_values_of_one(tds)

            if result_value["over10billioYn"] == "Y":
                break

        # return
        return result_value
    except Exception as ex:
        logger.error("ERROR!!!!: find_stock_values_of_one_page")
        logger.error(ex)


###########################################################
# Main 처리: 주식 기본 테이블에서 data 읽어서 이를 처리한다.
###########################################################
def main_process(stc_id):

    last_page = get_last_page_of_stock(stc_id)
    for page in range(1, last_page+1):
        result_value = find_stock_values_of_one_page(stc_id, page)

        if result_value["over10billioYn"] == "Y":
            break

    return result_value


if __name__ == "__main__":
    main_process('20190625')
