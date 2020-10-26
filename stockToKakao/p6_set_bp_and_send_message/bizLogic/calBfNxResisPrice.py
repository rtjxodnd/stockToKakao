from stockToKakao.commonModule.calcModule import stringToList


# 종목 스크린 main
def cal_before_next_price(now_price, resistance_price):
    # 초기값
    before_price_new = 0
    next_price_new = 99999999

    # 새로운 이전 전고점, 다음전고점 세팅
    resistance_price_list = stringToList(resistance_price)
    for resistance_price_unit in resistance_price_list:
        if int(resistance_price_unit) > now_price:
            next_price_new = int(resistance_price_unit)
            break
        before_price_new = int(resistance_price_unit)

    # 결과리턴
    return {'before_price': before_price_new, 'next_price': next_price_new}


if __name__ == '__main__':
    print(cal_before_next_price())
