from flask import Flask, render_template, request
import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import dbModule, ipModule


app = Flask(__name__)


@app.route('/')
def index():
    ip = ipModule.get_ip()['ip']
    return render_template('index.html', ip=ip)


@app.route('/oauth')
def oauth():
    code = str(request.args.get('code'))
    # resToken = getAccessToken("3395ba66a46252d72dd58bbdeae94bd2", str(code))
    resToken = getAccessToken("c1889aaa44f7ace2b5e149d9e6c1433d", str(code))

    db_class = dbModule.Database()
    sql = "DELETE from stock_search.kakao_token"
    db_class.execute(sql)

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


def getAccessToken(clientId, code):  # 세션 코드값 code 를 이용해서 ACESS TOKEN과 REFRESH TOKEN을 발급 받음
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')