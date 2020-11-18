from stockToKakao.p6_set_bp_and_send_message.crawler.crawlDailyStockPriceInfo import main_process as daily_stock_price_info
from datetime import datetime


# 종목 스크린 main
def increase_yn(stc_id):
    print(stc_id+"판별")
    # 전달값 저장
    tdy_prices_info = daily_stock_price_info(stc_id)[0]
    bf1_prices_info = daily_stock_price_info(stc_id)[1]

    # 거래량 없으면 false리턴
    if tdy_prices_info['dealAmt'] == 0 or bf1_prices_info['dealAmt'] == 0:
        return False

    # 금일 상승 아니면 false리턴
    if float(tdy_prices_info['opn_price']) >= float(tdy_prices_info['cls_price']):
        return False

    # 당일 거래량이 전거래일 거래량보다 상승 안했으면 false 리턴
    # 기준: 10시 이전 100%, 11시 이전 150%, 12시 이전 200%, 13시 이전 250%, 14시 이전 300%, 15시 이전 350%, 16시 이전 400%
    now_time = int(datetime.today().strftime("%H%M%S")[0:2])
    if now_time <= 10 and tdy_prices_info['dealAmt'] < bf1_prices_info['dealAmt']*1.0:
        return False
    elif now_time <= 11 and tdy_prices_info['dealAmt'] < bf1_prices_info['dealAmt']*1.5:
        return False
    elif now_time <= 12 and tdy_prices_info['dealAmt'] < bf1_prices_info['dealAmt']*2.0:
        return False
    elif now_time <= 13 and tdy_prices_info['dealAmt'] < bf1_prices_info['dealAmt']*2.5:
        return False
    elif now_time <= 14 and tdy_prices_info['dealAmt'] < bf1_prices_info['dealAmt']*3.0:
        return False
    elif now_time <= 15 and tdy_prices_info['dealAmt'] < bf1_prices_info['dealAmt']*3.5:
        return False
    elif now_time <= 16 and tdy_prices_info['dealAmt'] < bf1_prices_info['dealAmt']*4.0:
        return False

    # 끝까지 모든 조건 충족시 True 리턴
    return True


if __name__ == '__main__':
    print(increase_yn('005930'))
