from bs4 import BeautifulSoup
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.chromedriver.setPageDriver import set_page_driver


# 한페이지의 data 추출
# sosok: 0코스닥, 1코스피
# page: 웹 페이지 지정
# stockOrder: 해당 페이지 내에서의 순서
def crawl_one_page_values(sosok=0, page=1):
    # 로거
    logger = logging.getLogger(__name__)

    try:
        # 데이터 탐색
        url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok="+str(sosok)+"&page="+str(page)

        driver = set_page_driver(url)
        bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()

        table = bs_obj.find("table", {"class": "type_2"})
        tbody = table.find("tbody")
        trs = tbody.find_all("tr", {"onmouseover": "mouseOver(this)"})

        # return
        return trs

    except Exception as ex:
        logger.error("ERROR!!!!: crawl_one_page_values")
        logger.error(ex)
