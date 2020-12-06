from stockToKakao.commonModule import dbModule
from stockToKakao.p4_capture_and_send_message.crawler.crawlDailyStockPriceInfo import main_process as daily_stock_price_info


# 종목 스크린 main
def decision_capture_stock(stc_id):
    # DB 모듈선언
    db_class = dbModule.Database()

    # 이평선 정보 조회
    sql = "select a.stc_id, a.ma5, a.ma20, a.ma60, a.ma120, a.ma240 " \
          "from stock_search.stock_move_avg a, stock_search.stock_basic b " \
          "where a.stc_id = b.stc_id and a.stc_id = '%s'" % stc_id
    row = db_class.executeOne(sql)

    # 전달값 저장
    tdy_prices_info = daily_stock_price_info(stc_id)[0]
    cls_price = float(tdy_prices_info['cls_price'])
    opn_price = float(tdy_prices_info['opn_price'])
    hig_price = float(tdy_prices_info['hig_price'])
    low_price = float(tdy_prices_info['low_price'])

    # DB 조회값
    ma20 = float(row['ma20'])

    # 종가가 20 이평선보다 아래에 있으면 현재가 리턴
    if cls_price < ma20:
        return cls_price

    # 저가가 20 이평선보다 아래에 있으면 현재가 리턴
    if low_price < ma20:
        return cls_price

    # 종가와 20이평선 차이가 2% 이내이면 현재가 리턴
    if (cls_price / ma20) <= 1.02:
        return cls_price

    # 저가와 20이평선 차이가 1% 이내이면 현재가 리턴
    if (low_price / ma20) <= 1.01:
        return cls_price

    # 끝까지 모든 조건 미충족시 0 리턴
    return 0


if __name__ == '__main__':
    print(decision_capture_stock('017040'))
