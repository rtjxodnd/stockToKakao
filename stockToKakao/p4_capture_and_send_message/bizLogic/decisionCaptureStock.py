from stockToKakao.commonModule import dbModule
from stockToKakao.p4_capture_and_send_message.crawler.crawlDailyStockPriceInfo import main_process as daily_stock_price_info


# 종목 스크린 main
def decision_capture_stock(stc_id, opn_price=0, hig_price=0, low_price=0, cls_price=0):
    # DB 모듈선언
    db_class = dbModule.Database()

    # 이평선 정보 조회
    sql = "select a.stc_id, a.ma5, a.ma20, a.ma60, a.ma120, a.ma240 " \
          "from stock_search.stock_move_avg a, stock_search.stock_basic b " \
          "where a.stc_id = b.stc_id and a.stc_id = '%s'" % stc_id
    row = db_class.executeOne(sql)

    # 전달값 저장
    tdy_prices_info = daily_stock_price_info(stc_id)[0]
    tdy_cls_price = float(tdy_prices_info['cls_price'])
    tdy_opn_price = float(tdy_prices_info['opn_price'])
    tdy_hig_price = float(tdy_prices_info['hig_price'])
    tdy_low_price = float(tdy_prices_info['low_price'])

    # DB 조회값
    ma20 = float(row['ma20'])

    # 종가가 20 이평선보다 위에 있으면 0 리턴
    if tdy_cls_price > ma20:
        return 0

    # 저가가 20 이평선보다 위에 있으면 0 리턴
    if tdy_low_price > ma20:
        return 0

    # 종가와 20이평선 차이가 2% 초과이면 0 리턴
    if (tdy_cls_price / ma20) > 1.03:
        return 0

    # 저가와 20이평선 차이가 1% 초과이면 0 리턴
    if (tdy_low_price / ma20) > 1.02:
        return 0

    # 종가가 가능성 판별일 종가보다 3% 초과인 경우 현재가 리턴
    if (tdy_cls_price / cls_price) > 1.03:
        return 0

    # 종가가 가능성 판별일 종가보다 3% 미달인 경우 현재가 리턴
    if (tdy_cls_price / cls_price) < 0.97:
        return 0

    # 끝까지 모든 조건 미충족시 0 리턴
    return tdy_cls_price


if __name__ == '__main__':
    print(decision_capture_stock('149980'))
#     095500, 149980, 017040
