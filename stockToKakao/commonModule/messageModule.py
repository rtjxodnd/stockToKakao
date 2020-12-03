import json
import requests
from stockToKakao.commonModule import dbModule


# 헤더세팅
def set_headers():
    # 토큰조회
    db_class = dbModule.Database()
    sql = "SELECT access_token from stock_search.kakao_token"
    row = db_class.executeOne(sql)

    # 헤더세팅
    headers = {
        "Authorization": "Bearer " + row['access_token']
    }
    return headers


# 데이터세팅
def set_data(stc_id, stc_name, text, uuids):
    data = {
        "receiver_uuids": json.dumps(uuids),
        "template_object": json.dumps({"object_type": "text",
                                       "text": text + "\n "
                                               "[" + stc_name + "]\n"
                                               " https://finance.naver.com/item/main.nhn?code=" + stc_id,
                                       "link": {
                                           "web_url": "https://www.daum.com/",
                                           "mobile_web_url": "https://www.daum.com/"},
                                       "button_title": "네이버증권 바로가기"
                                       })}
    print('\n송신대상: ' + stc_id + "[" + stc_name + "]")

    return data


# 친구목록수신
def get_friends(headers):
    url = "https://kapi.kakao.com/v1/api/talk/friends"
    result = json.loads(requests.get(url, headers=headers).text)
    uuids = []

    friends_list = result.get("elements")
    print("수신 친구 목록")
    for friend in friends_list:
        print(friend['profile_nickname'], friend['uuid'])
        uuids.append(friend['uuid'])
    return uuids


# 나에게 메시지송신
def send_message_to_myself(headers, data):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    response = requests.post(url, headers=headers, data=data)
    if response.json().get('result_code') == 0:
        print('나에게 메시지를 성공적으로 보냈습니다.')
    else:
        print('나에게 메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))


# 친구에게 메시지송신
def send_message_to_friends(headers, data):
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    response = requests.post(url, headers=headers, data=data)

    if response.json().get('code') is None:
        print('친구에게 메시지를 성공적으로 보냈습니다.')
    else:
        print('친구에게 메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))
        print('나에게 메시지 보내기 수행')
        send_message_to_myself(headers, data)
