from bs4 import BeautifulSoup
import traceback
import requests
from stockToKakao.chromedriver.setPageDriver import set_page_driver


# 한건의 data 추출
def getStockNowPrice(stc_id):
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

        # 요약정보
        highInfo = bs_obj.find("table", {"class": "no_info"}).find_all("tr")[0].find_all("td")[1]
        lowInfo = bs_obj.find("table", {"class": "no_info"}).find_all("tr")[1].find_all("td")[1]

        # 현재가
        now_price = contentInfo.find_all("span")[0].text.replace(",", "")

        # 고가
        high_price = highInfo.find_all("span", {"class": "blind"})[0].text.replace(",", "")

        # 저가
        low_price = lowInfo.find_all("span", {"class": "blind"})[0].text.replace(",", "")

        # 필요 데이터 추출
        result_value = {"now_price": now_price, "high_price": high_price, "low_price": low_price}

        return result_value
    except Exception as ex:
        print("ERROR!!!!: getStockNowPrice")
        traceback.print_exc()


if __name__ == '__main__':
    print(getStockNowPrice('005930'))
