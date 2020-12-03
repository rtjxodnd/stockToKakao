import numpy as np


# '/'로 구분지어진 문자열을 리스트로 변환함.
def stringToList (strInput):

    listOutput = strInput.split('/')
    del listOutput[-1:]

    for i, value in enumerate(listOutput):
        listOutput[i] = float(value)

    listOutput.sort()

    return listOutput


# 리스트를 '/'로 구분지어진 문자열로 변환함.
def listToString (listInput):

    strOutput = ''

    for unit in listInput:
        strOutput = strOutput + str(unit) + '/'

    return strOutput


# outlier data 제거
def remove_outlier(input_list=None, weight=1.5):
    # target 값과 상관관계가 높은 열을 우선적으로 진행
    quantile_25 = np.percentile(input_list, 25)
    quantile_75 = np.percentile(input_list, 75)

    IQR = quantile_75 - quantile_25
    IQR_weight = IQR * weight

    lowest = quantile_25 - IQR_weight
    highest = quantile_75 + IQR_weight

    remove_outlier_data = []
    for input_value in input_list:
        if input_value < lowest or input_value > highest:
            continue
        remove_outlier_data.append(float(input_value))

    return remove_outlier_data


# 1호가 단위가격 산출
def getTikPrice(stc_dvsn, now_price):

    tikPrice = 0

    if now_price < 1000:
        tikPrice = 1
    elif now_price < 5000:
        tikPrice = 5
    elif now_price < 10000:
        tikPrice = 10
    elif now_price < 50000:
        tikPrice = 50
    elif now_price < 100000:
        tikPrice = 100
    elif now_price < 500000:
        if stc_dvsn == '01':
            tikPrice = 500
        elif stc_dvsn == '02':
            tikPrice = 100
    else:
        if stc_dvsn == '01':
            tikPrice = 1000
        elif stc_dvsn == '02':
            tikPrice = 100

    return tikPrice


# outlier data 제거
def remove_outlier(input_list=None, weight=1.5):
    # target 값과 상관관계가 높은 열을 우선적으로 진행
    quantile_25 = np.percentile(input_list, 25)
    quantile_75 = np.percentile(input_list, 75)

    IQR = quantile_75 - quantile_25
    IQR_weight = IQR * weight

    lowest = quantile_25 - IQR_weight
    highest = quantile_75 + IQR_weight

    remove_outlier_data = []
    for input_value in input_list:
        if input_value < lowest or input_value > highest:
            continue
        remove_outlier_data.append(float(input_value))

    return remove_outlier_data


# 변이계수, coefficient of variation, CV
def coefficient_of_variation(valList):
    # 평균
    avg = np.mean(valList)

    # 표준편차
    std = np.std(valList)

    # 변이계수
    cv = round(std / avg * 100, 2)

    # 결과리턴
    return {"avg": avg, "std": std, "cv": cv}


# 리스트 자르기
def divide_list(in_list, n):
    # 리스트 l의 길이가 n이면 계속 반복
    for i in range(0, len(in_list), n):
        yield in_list[i:i + n]
