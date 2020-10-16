from stockToKakao.p3_get_filtered_stock_info.crawler.crawlStockDetailInfo import getStockDetailInfo
from stockToKakao.p3_get_filtered_stock_info.crawler.crawlDailyStockInfo import main_process as maxVolumeCrawler
from stockToKakao.p3_get_filtered_stock_info.crawler.crawlImpairedRatio import find_impaired_ratio


# 평균값 산출
def calculator_avg(factors):
    # 초기값 설정
    tot_sum = 0  # 피제수설정
    j = 0  # 제수설정

    # 숫자 변환 및 제수 절정
    for i in factors:
        if factors[i] == "\xa0" or factors[i] == "-" or factors[i] == "":
            factors[i] = 0
        else:
            factors[i] = float(factors[i].replace(",", ""))
            j += 1

    # 합계값
    for i in factors:
        # 과거 데이터 중 하나라도 음수 있으면 0 리턴하고 종료.
        tot_sum += factors[i]

    # 제수가 0이면 roe = 0 리턴
    if j == 0:
        return {"avg": 0}

    # 평균값 계산
    avg = tot_sum / j

    return {"avg": avg}


# 음수검증
def calculator_recent(factors):
    # 숫자 변환 및 제수 절정
    for i in factors:

        if factors[i] == "\xa0" or factors[i] == "-" or factors[i] == "":
            factors[i] = 0
        else:
            factors[i] = float(factors[i])

        # 하나라도 음수 있으면 -1 리턴하고 종료.
        if factors[i] < 0:
            return {"recent": -1}
    return {"recent": 1}


###########################################################
# Main 처리: data 읽어서 필터링한다.
###########################################################
def main_process(stc_id):

    try:
        # data추출
        crawling_data = getStockDetailInfo(stc_id)
        now_price = crawling_data["now_price"]
        price_high_52week = crawling_data["price_high_52week"]
        price_low_52week = crawling_data["price_low_52week"]
        sales_accounts = crawling_data["sales_accounts"]
        operating_profits = crawling_data["operating_profits"]
        net_incomes = crawling_data["net_incomes"]
        op_margins = crawling_data["op_margins"]
        net_margins = crawling_data["net_margins"]
        roes = crawling_data["roes"]
        debt_ratios = crawling_data["debt_ratios"]
        quick_ratios = crawling_data["quick_ratios"]
        reservation_rate = crawling_data["reservation_rates"]
        sales_accounts_recent = crawling_data["sales_accounts_recent"]
        operating_profits_recent = crawling_data["operating_profits_recent"]
        net_incomes_recent = crawling_data["net_incomes_recent"]
        op_margins_recent = crawling_data["op_margins_recent"]
        net_margins_recent = crawling_data["net_margins_recent"]
        roes_recent = crawling_data["roes_recent"]
        debt_ratios_recent = crawling_data["debt_ratios_recent"]
        quick_ratios_recent = crawling_data["quick_ratios_recent"]
        reservation_rate_recent = crawling_data["reservation_rates_recent"]

        # 평균값 산출
        avg_sales_account = calculator_avg(sales_accounts)["avg"]
        avg_operating_profit = calculator_avg(operating_profits)["avg"]
        avg_net_income = calculator_avg(net_incomes)["avg"]
        avg_op_margin = calculator_avg(op_margins)["avg"]
        avg_net_margin = calculator_avg(net_margins)["avg"]
        avg_roe = calculator_avg(roes)["avg"]
        avg_debt_ratios = calculator_avg(debt_ratios)["avg"]
        avg_quick_ratios = calculator_avg(quick_ratios)["avg"]
        avg_reservation_rate = calculator_avg(reservation_rate)["avg"]

        # 음수검증(년단위)
        sales_account_recent = calculator_recent(sales_accounts)["recent"]
        operating_profit_recent = calculator_recent(operating_profits)["recent"]
        net_income_recent = calculator_recent(net_incomes)["recent"]
        op_margin_recent = calculator_recent(op_margins)["recent"]
        net_margin_recent = calculator_recent(net_margins)["recent"]
        roe_recent = calculator_recent(roes)["recent"]

        # 52주 최저가의 2배가 현재가 보다 작으면 매수 안함
        if float(price_low_52week) * 2 < float(now_price):
            return False
        # 최근 매출액 중 음수가 있으면 매수 안함
        if sales_account_recent < 0:
            return False
        # 최근 영업이익 중 음수가 있으면 매수 안함
        if operating_profit_recent < 0:
            return False
        # 영업이익이 2년간 1.5배 미만 상승 안했으면 매수 안 함
        # if float(operating_profits["operating_profit0"])*1.5 > float(operating_profits["operating_profit2"]):
        #     continue
        # 당기순이익 평균이 0보다 작으면 매수 안함
        if avg_net_income < 0:
            return False
        # 부채율이 150보다 크면 매수 안함
        if avg_debt_ratios > 150:
            return False
        # 유보율이 100보다 작으면 매수 안함
        if avg_quick_ratios < 100:
            return False
        # 자본잠식률 45퍼센트 이상이면 매수 안 함
        impaired_info = find_impaired_ratio(stc_id, 45)
        if impaired_info["impaired_yn"] == "Y":
            return False
        # 3년이내 일거래 100억 존재 안하면 매수 안함
        max_deal_amt_info = maxVolumeCrawler(stc_id)
        if max_deal_amt_info["over10billioYn"] == "N":
            return False

    except Exception as e:
        print(stc_id)
        print(e)
        return False

    # 끝까지 모든 조건 충족시 True 리턴
    return True


if __name__ == '__main__':
    print(main_process('005930'))
