from stockToKakao.p4_capture_and_send_message.crawler.crawlDailyStockPriceInfo import main_process as daily_stock_price_info


# 종목 스크린 main
def decision_possible_stock(stc_id):
    # 전달값 저장
    tdy_prices_info = daily_stock_price_info(stc_id)[0]
    bf1_prices_info = daily_stock_price_info(stc_id)[1]
    bf2_prices_info = daily_stock_price_info(stc_id)[2]
    bf3_prices_info = daily_stock_price_info(stc_id)[3]
    bf4_prices_info = daily_stock_price_info(stc_id)[4]

    # 거래량 없으면 0리턴
    if tdy_prices_info['dealAmt'] == 0 or bf1_prices_info['dealAmt'] == 0 or bf2_prices_info['dealAmt'] == 0:
        return {"cls_price": 0, "low_price": 0, "opn_price": 0, "hig_price": 0, "dealQnt": 0}

    # 1전거래일 상승 아니면 0리턴
    if float(bf1_prices_info['opn_price']) >= float(bf1_prices_info['cls_price']):
        return {"cls_price": 0, "low_price": 0, "opn_price": 0, "hig_price": 0, "dealQnt": 0}

    # 전거래일 거래량이 2전거래일 거래량보다 500% 상승 안했으면 0리턴
    if bf1_prices_info['dealAmt'] < bf2_prices_info['dealAmt']*5:
        return {"cls_price": 0, "low_price": 0, "opn_price": 0, "hig_price": 0, "dealQnt": 0}

    # 당일 거래량이 전거래일 거래량보다 25% 이상 하락 안했으면 0리턴
    if tdy_prices_info['dealAmt'] > bf1_prices_info['dealAmt']/4:
        return {"cls_price": 0, "low_price": 0, "opn_price": 0, "hig_price": 0, "dealQnt": 0}

    # 당일 종가가 5일 평균 하회 하면 0리턴
    avg_5 = (float(tdy_prices_info['cls_price']) +
             float(bf1_prices_info['cls_price']) +
             float(bf2_prices_info['cls_price']) +
             float(bf3_prices_info['cls_price']) +
             float(bf4_prices_info['cls_price'])) / 5
    if float(tdy_prices_info['cls_price']) < avg_5:
        return {"cls_price": 0, "low_price": 0, "opn_price": 0, "hig_price": 0, "dealQnt": 0}

    # 끝까지 모든 조건 충족시 당일종가 및 전 거래량 리턴
    return {"cls_price": float(tdy_prices_info['cls_price']),
            "low_price": float(tdy_prices_info['low_price']),
            "opn_price": float(tdy_prices_info['opn_price']),
            "hig_price": float(tdy_prices_info['hig_price']),
            "dealQnt": bf1_prices_info['dealQnt']}


if __name__ == '__main__':
    print(decision_possible_stock('289010'))
