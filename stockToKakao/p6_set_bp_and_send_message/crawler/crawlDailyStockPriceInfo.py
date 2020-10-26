# https://finance.naver.com 으로부터 일별 종가정보를 크롤링한다.

# 필요라이브러리 import
import requests
from bs4 import BeautifulSoup
import logging
from stockToKakao.chromedriver.setPageDriver import set_page_driver


# 공통변수
FINANCE_URL = "https://finance.naver.com/item/sise_day.nhn?code="


# 한건의 data 추출
# tds: 입력된 tds data
# stockOrder: 해당 페이지 내에서의 순서
def find_stock_values_of_one(tds):

    # 필요 데이터 추출
    base_dt = tds[0].find("span").text.replace(".", "")  # 기준일
    cls_price = tds[1].find("span").text.replace(",", "")  # 금일종가
    opn_price = tds[3].find("span").text.replace(",", "")  # 시가
    hig_price = tds[4].find("span").text.replace(",", "")  # 고가
    low_price = tds[5].find("span").text.replace(",", "")  # 저가
    deal_qnt = tds[6].text.replace(",", "")  # 거래량
    deal_amt = float(cls_price) * float(deal_qnt)  # 거래금액

    # 결과세팅
    result_value = {"baseDt": base_dt,
                    "cls_price": cls_price,
                    "opn_price": opn_price,
                    "hig_price": hig_price,
                    "low_price": low_price,
                    "dealAmt": deal_amt}

    # return
    return result_value


# 한개 page 처리
def find_stock_values_of_one_page(stock_id):
    # 로거
    logger = logging.getLogger(__name__)

    try:
        # 데이터 탐색
        url = FINANCE_URL+stock_id+"&page=1"
        page_call_result = requests.get(url)
        bs_obj = BeautifulSoup(page_call_result.content, "html.parser")
        # driver = set_page_driver(url)
        # bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
        # driver.close()

        trs = bs_obj.find_all("tr", {"onmouseover": "mouseOver(this)"})

        # 필요 데이터 추출
        result_value = []
        for order in range(0, 5):
            tr = trs[order]
            tds = tr.find_all("td")
            result_value.append(find_stock_values_of_one(tds))

        # return
        return result_value

    except Exception as ex:
        logger.error("ERROR!!!!: find_stock_values_of_one_page")
        logger.error(ex)


###########################################################
# Main 처리: 주식 기본 테이블에서 data 읽어서 이를 처리한다.
###########################################################
def main_process(stc_id):

    result_value = find_stock_values_of_one_page(stc_id)
    return result_value


if __name__ == "__main__":
    main_process('005930')
