from stockToKakao.p4_capture_and_send_message.crawler.crawlDailyStockPriceInfo import main_process as daily_stock_price_info


# 종목 스크린 main
def capture_stock(stc_id):
    # 전달값 저장
    tdy_prices_info = daily_stock_price_info(stc_id)[0]
    bf1_prices_info = daily_stock_price_info(stc_id)[1]
    bf2_prices_info = daily_stock_price_info(stc_id)[2]
    bf3_prices_info = daily_stock_price_info(stc_id)[3]
    bf4_prices_info = daily_stock_price_info(stc_id)[4]

    # 거래량 없으면 false리턴
    if tdy_prices_info['dealAmt'] == 0 or bf1_prices_info['dealAmt'] == 0 or bf2_prices_info['dealAmt'] == 0:
        return False

    # 1전거래일 상승 아니면 false리턴
    if float(bf1_prices_info['opn_price']) >= float(bf1_prices_info['cls_price']):
        return False

    # 전거래일 거래량이 2전거래일 거래량보다 500% 상승 안했으면 false 리턴
    if bf1_prices_info['dealAmt'] < bf2_prices_info['dealAmt']*5:
        return False

    # 당일 거래량이 전거래일 거래량보다 25% 이상 하락 안했으면 false 리턴
    if tdy_prices_info['dealAmt'] > bf1_prices_info['dealAmt']/4:
        return False

    # 당일 종가가 5일 평균 하회 하면 false 리턴
    avg_5 = (float(tdy_prices_info['cls_price']) +
             float(bf1_prices_info['cls_price']) +
             float(bf2_prices_info['cls_price']) +
             float(bf3_prices_info['cls_price']) +
             float(bf4_prices_info['cls_price'])) / 5
    if float(tdy_prices_info['cls_price']) < avg_5:
        return False

    # 끝까지 모든 조건 충족시 True 리턴
    return True


if __name__ == '__main__':
    print(capture_stock('005930'))
