from stockToKakao.p12_set_ma_and_send_message.crawler.crawlDailyStockInfo import crawl_daily_stock_info as dailyInfo


# 이동평균값 구하기
def cal_move_avg_values(stc_id):
    close_values = dailyInfo(stc_id, 240)['종가']
    now_price = close_values.head(1).mean()
    ma5 = round(close_values.head(5).mean(), 2)
    ma20 = round(close_values.head(20).mean(), 2)
    ma60 = round(close_values.head(60).mean(), 2)
    ma120 = round(close_values.head(120).mean(), 2)
    ma240 = round(close_values.head(240).mean(), 2)

    # return
    return {"now_price": now_price, "ma5": ma5, "ma20": ma20, "ma60": ma60, "ma120": ma120, "ma240": ma240}


if __name__ == "__main__":
    print(cal_move_avg_values('005930'))

