import numpy as np
from sklearn.cluster import DBSCAN
import math
from stockToKakao.commonModule.calcModule import getTikPrice, remove_outlier


# 종목 스크린 main
def cal_before_resistance_price(stc_dvsn, now_price, hiLoList):
    # 함수호출 위한 reshape
    x = np.reshape(hiLoList, (-1, 1))

    # 함수 사용해서 이상치 값 삭제
    remove_outlier_x = remove_outlier(input_list=x, weight=1.5)
    remove_outlier_x = np.reshape(remove_outlier_x, (-1, 1))

    # 해당가격 의 호가 산출
    ticPrice = getTikPrice(stc_dvsn, now_price)

    # DBSCAN의 적정인자 세팅
    eps_value = ticPrice*2  # 2틱
    min_samples_value = math.floor(len(x) / 2 / 10)  # 기간의 1/10

    # 군집알고리즘 수행
    db = DBSCAN(eps=eps_value, min_samples=min_samples_value, metric='euclidean')
    y_db = db.fit_predict(remove_outlier_x)

    # 그룹의 유니크한 값 추출
    y_db_list = list(set(y_db))

    # 유효한 군집 대표값 추출
    result_values = []
    for group in y_db_list:
        x_values = 0
        cnt = 0
        if group == -1:
            continue
        for i, value in enumerate(y_db):
            if value == group:
                x_values += remove_outlier_x[i]
                cnt += 1
        result_values.append(round(float(x_values / cnt)))
    result_values.sort()

    # 결과리턴
    return result_values


if __name__ == '__main__':
    print(cal_before_resistance_price('005930'))
