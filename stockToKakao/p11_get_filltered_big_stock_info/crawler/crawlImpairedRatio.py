from bs4 import BeautifulSoup
import requests
import logging


# 한건의 data 추출
def find_impaired_ratio(stc_id, base_ratio = 45):
    # 로거
    logger = logging.getLogger(__name__)

    try:
        # 데이터 탐색
        url = "https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A"+str(stc_id)\
              +"&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN="
        page_call_result = requests.get(url)
        bs_obj = BeautifulSoup(page_call_result.content.decode('utf-8', 'replace'), "html.parser")

        # 시세정보
        priceInfo = bs_obj.find("body")\
            .find("div", {"class": "ul_wrap", "id": "div1"})\
            .find("div", {"class": "um_table", "id": "svdMainGrid1"}) \
            .find("table", {"class": "us_table_ty1 table-hb thbg_g h_fix zigbg_no"})\
            .find("tbody")

        # 재무정보
        fianacialInfo = bs_obj.find("body")\
            .find("div", {"class": "ul_wrap", "id": "div15"})\
            .find("div", {"class": "um_table", "id": "highlight_D_A"}) \
            .find("table", {"class": "us_table_ty1 h_fix zigbg_no"})\
            .find("tbody")

        # 유통주식수
        num_of_circulation = float(priceInfo.find_all("tr")[5].find_all("td")[1].text.replace(",", "").split("/")[0])

        # 과년도 자본총계
        total_capital = fianacialInfo.find_all("tr")[8].find_all("td")[2].text.replace(",", "")

        # 과년도 자본금
        capital = fianacialInfo.find_all("tr")[11].find_all("td")[2].text.replace(",", "")

        # 자본잠식률: (자본금-자본총계)/자본금*100
        impaired_ratio = round((float(capital)-float(total_capital))/float(capital)*100, 2)
        impaired_yn = "N"
        if impaired_ratio > base_ratio:
            impaired_yn = "Y"

        # 필요 데이터 추출
        result_value = {"impaired_yn": impaired_yn,
                        "impaired_ratio": impaired_ratio,
                        "num_of_circulation": num_of_circulation}

        return result_value

    except Exception as ex:
        logger.error("ERROR!!!!: find_impaired_ratio")
        logger.error(ex)


if __name__ == '__main__':
    print(find_impaired_ratio('082920'))
