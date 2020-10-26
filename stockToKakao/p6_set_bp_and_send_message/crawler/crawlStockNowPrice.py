from bs4 import BeautifulSoup
import logging
import requests
from stockToKakao.chromedriver.setPageDriver import set_page_driver


# 한건의 data 추출
def getStockNowPrice(stc_id):
    # 로거
    logger = logging.getLogger(__name__)

    try:
        # 데이터 탐색
        url = "https://finance.naver.com/item/main.nhn?code=" + str(stc_id)
        page_call_result = requests.get(url)
        bs_obj = BeautifulSoup(page_call_result.content.decode('euc-kr', 'replace'), "html.parser")

        # driver = set_page_driver(url)
        # bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
        # driver.close()

        # 현재가정보
        contentInfo = bs_obj.find("div", {"id": "content"}).find("p", {"class": "no_today"}).find("em")

        # 현재가
        now_price = contentInfo.find_all("span")[0].text.replace(",", "")

        # 필요 데이터 추출
        result_value = {"now_price": now_price}

        return result_value
    except Exception as ex:
        logger.error("ERROR!!!!: getStockNowPrice")
        logger.error(ex)


if __name__ == '__main__':
    print(getStockNowPrice('005930'))
