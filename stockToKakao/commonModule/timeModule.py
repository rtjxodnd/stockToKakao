from stockToKakao.commonModule import ipModule
from datetime import datetime


# 로컬 및 aws 서버간 시간이 다르므로 이를 표준화 하는 시간 필요
def get_server_time():
    ip_name = ipModule.get_ip()['ip_name']
    time = datetime.today().strftime("%H%M%S")
    timeDiff = 9

    # 로컬서버인 경우는 그대로 사용, aws의 경우는 9시간을 더해줌.
    if ip_name == 'localServer':
        stdTime = time
    elif ip_name == 'awsServer':
        stdTime = repr(int(time[0:2])+timeDiff).zfill(2)+time[-4:]

    return stdTime


if __name__ == "__main__":
    print(get_server_time())
