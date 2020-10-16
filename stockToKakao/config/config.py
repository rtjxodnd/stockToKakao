from stockToKakao.commonModule import ipModule


# chromeDriverPath return
def chromeDriverPath():
    ip_name = ipModule.get_ip()['ip_name']

    if ip_name == "localServer":
        chromeDriverPath = "C:/Users/rtjxo/PycharmProjects/stockToKakao/stockToKakao/chromedriver/chromedriver_windows.exe"
    elif ip_name == "awsServer":
        chromeDriverPath = "/home/ubuntu/projects/stockToKakao/chromedriver/chromedriver_ubuntu"
    else:
        chromeDriverPath = "/home/ubuntu/projects/stockToKakao/chromedriver/chromedriver_ubuntu"

    return chromeDriverPath