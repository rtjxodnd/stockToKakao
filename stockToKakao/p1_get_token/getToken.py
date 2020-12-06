from flask import Flask, render_template, request
import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule, ipModule, messageModule


app = Flask(__name__)


@app.route('/')
def index():
    ip = ipModule.get_ip()['ip']
    return render_template('index.html', ip=ip)


@app.route('/oauth')
def oauth():
    code = str(request.args.get('code'))
    resToken = getAccessToken("c1889aaa44f7ace2b5e149d9e6c1433d", str(code))
    result = getUserInfo(resToken)

    # owner가 아니면 리턴
    if result['id'] != 1535632259:
        return '로그인 및 약관동의 완료!! \n 이제 카카오톡에서 findstockgogo 친구추가 해주세요.'

    # 기존 owner 계정 토큰 제거
    db_class = dbModule.Database()
    sql = "DELETE from stock_search.kakao_token"
    db_class.execute(sql)

    # 신규 owner 계정 토큰 저장
    sql = "INSERT INTO stock_search.kakao_token(" \
          "code, " \
          "access_token, " \
          "token_type, " \
          "refresh_token, " \
          "expires_in, " \
          "scope, " \
          "refresh_token_expires_in) " \
          "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (str(code),  str(resToken['access_token']),  str(resToken['token_type']),
           str(resToken['refresh_token']),  str(resToken['expires_in']),
           str(resToken['scope']),  str(resToken['refresh_token_expires_in']))
    db_class.execute(sql)
    db_class.commit()

    return '토큰발급 완료!!' + \
           '<br/>code=' + str(code) + \
           '<br/>access_token=' + str(resToken['access_token']) + \
           '<br/>token_type=' + str(resToken['token_type']) + \
           '<br/>refresh_token=' + str(resToken['refresh_token']) + \
           '<br/>expires_in=' + str(resToken['expires_in']) + \
           '<br/>scope=' + str(resToken['scope']) + \
           '<br/>refresh_token_expires_in=' + str(resToken['refresh_token_expires_in'])


# 세션 코드값 code 를 이용해서 ACESS TOKEN과 REFRESH TOKEN을 발급 받음
def getAccessToken(clientId, code):
    ip = ipModule.get_ip()['ip']
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code"
    payload += "&client_id=" + clientId
    payload += "&redirect_url=http%3A%2F%2F"+ip+"%3A5000%2Foauth&code=" + code
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    reponse = requests.request("POST", url, data=payload, headers=headers)
    access_token = json.loads(((reponse.text).encode('utf-8')))
    return access_token


# ACESS TOKEN 이용하여 로그인한 사용자 ID 식별
def getUserInfo(resToken):
    url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": "Bearer " + str(resToken['access_token'])}

    result = json.loads(requests.get(url, headers=headers).text)
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
