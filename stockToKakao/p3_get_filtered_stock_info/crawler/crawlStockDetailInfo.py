from bs4 import BeautifulSoup
import logging
import requests
from stockToKakao.chromedriver.setPageDriver import set_page_driver


# 한건의 data 추출
def getStockDetailInfo(stc_id):
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

        # 보조사이드 정보
        asideInfo = bs_obj.find("div", {"id": "aside"}).find("div", {"class": "aside_invest_info"}).find("div", {"id": "tab_con1"})

        # 투자의견정보
        opinion = asideInfo.find_all("div")[4].find("table", {"summary": "투자의견 정보", "class": "rwidth"})

        # 분석 table
        analysis = bs_obj.find("div", {"class": "section cop_analysis"}).find("div", {"class": "sub_section"}).find("tbody").find_all("tr")

        # 현재가
        # now_price = ""
        # now_price_list = contentInfo.find_all("span")
        # for now_price_element in now_price_list:
        #     now_price = now_price + now_price_element.text.replace(",", "")
        now_price = contentInfo.find_all("span")[0].text.replace(",", "")

        # 52주 최고/최저가
        price52week = opinion.find_all("tr")[1].find("td")
        price_high_52week = price52week.find_all("em")[0].text.replace(",", "")
        price_low_52week = price52week.find_all("em")[1].text.replace(",", "")

        # 재무요약
        sales_accounts = analysis[0].find_all("td")
        operating_profits = analysis[1].find_all("td")
        net_incomes = analysis[2].find_all("td")
        op_margins = analysis[3].find_all("td")
        net_margins = analysis[4].find_all("td")
        roes = analysis[5].find_all("td")
        debt_ratios = analysis[6].find_all("td")
        quick_ratios = analysis[7].find_all("td")
        reservation_rate = analysis[8].find_all("td")

        # 필요 데이터 추출
        result_value = {"now_price": now_price,
                        "price_high_52week": price_high_52week,
                        "price_low_52week": price_low_52week,
                        "sales_accounts":
                            {"sales_account0": sales_accounts[0].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "sales_account1": sales_accounts[1].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "sales_account2": sales_accounts[2].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "sales_account3": sales_accounts[3].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "operating_profits":
                            {"operating_profit0": operating_profits[0].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "operating_profit1": operating_profits[1].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "operating_profit2": operating_profits[2].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "operating_profit3": operating_profits[3].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "net_incomes":
                            {"net_income0": net_incomes[0].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "net_income1": net_incomes[1].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "net_income2": net_incomes[2].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "net_income3": net_incomes[3].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "op_margins":
                            {"op_margin0": op_margins[0].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "op_margin1": op_margins[1].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "op_margin2": op_margins[2].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "op_margin3": op_margins[3].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "net_margins":
                            {"net_margin0": net_margins[0].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "net_margin1": net_margins[1].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "net_margin2": net_margins[2].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "net_margin3": net_margins[3].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "roes":
                            {"roe0": roes[0].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "roe1": roes[1].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "roe2": roes[2].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "roe3": roes[3].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "debt_ratios":
                            {"debt_ratio0": debt_ratios[0].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "debt_ratio1": debt_ratios[1].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "debt_ratio2": debt_ratios[2].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "debt_ratio3": debt_ratios[3].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "quick_ratios":
                            {"quick_ratio0": quick_ratios[0].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "quick_ratio1": quick_ratios[1].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "quick_ratio2": quick_ratios[2].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "quick_ratio3": quick_ratios[3].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "reservation_rates":
                            {"reservation_rate0": reservation_rate[0].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "reservation_rate1": reservation_rate[1].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "reservation_rate2": reservation_rate[2].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "reservation_rate3": reservation_rate[3].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "sales_accounts_recent":
                            {"sales_account7": sales_accounts[7].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "sales_account8": sales_accounts[8].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "sales_account9": sales_accounts[9].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "operating_profits_recent":
                            {"operating_profit7": operating_profits[7].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "operating_profit8": operating_profits[8].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "operating_profit9": operating_profits[9].text.replace("\n", "").replace("\t", "").replace(",","")},
                        "net_incomes_recent":
                            {"net_income7": net_incomes[7].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "net_income8": net_incomes[8].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "net_income9": net_incomes[9].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "op_margins_recent":
                            {"op_margin7": op_margins[7].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "op_margin8": op_margins[8].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "op_margin9": op_margins[9].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "net_margins_recent":
                            {"net_margin7": net_margins[7].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "net_margin8": net_margins[8].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "net_margin9": net_margins[9].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "roes_recent":
                            {"roe7": roes[7].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "roe8": roes[8].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "roe9": roes[9].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "debt_ratios_recent":
                            {"debt_ratio7": debt_ratios[7].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "debt_ratio8": debt_ratios[8].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "debt_ratio9": debt_ratios[9].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "quick_ratios_recent":
                            {"quick_ratio7": quick_ratios[7].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "quick_ratio8": quick_ratios[8].text.replace("\n", "").replace("\t", "").replace(",", ""),
                             "quick_ratio9": quick_ratios[9].text.replace("\n", "").replace("\t", "").replace(",", "")},
                        "reservation_rates_recent":
                            {"reservation_rate7": reservation_rate[7].text.replace("\n", "").replace("\t", "").replace(",",""),
                             "reservation_rate8": reservation_rate[8].text.replace("\n", "").replace("\t", "").replace(",",""),
                             "reservation_rate9": reservation_rate[9].text.replace("\n", "").replace("\t", "").replace(",","")}
                        }

        return result_value
    except Exception as ex:
        logger.error("ERROR!!!!: getStockDetailInfo")
        logger.error(ex)


if __name__ == '__main__':
    print(getStockDetailInfo('005930'))
