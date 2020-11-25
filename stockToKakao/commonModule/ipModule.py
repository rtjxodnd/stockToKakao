import socket


def get_ip():
    in_ip = socket.gethostbyname(socket.gethostname())

    # aws 인 경우와 로컬pc 인경우
    if in_ip == '172.31.6.179':
        ex_ip = {'ip': '13.209.83.184', 'ip_name': 'awsServer'}
    else:
        ex_ip = {'ip': 'localhost', 'ip_name': 'localServer'}

    return ex_ip
