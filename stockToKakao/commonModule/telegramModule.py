import telegram
from stockToKakao.commonModule import dbModule

# 데이터세팅
def set_data(stc_id, stc_name, text):
    data = text + "\n " \
            "[" + stc_name + "]\n  " \
            "https://finance.naver.com/item/main.nhn?code=" + stc_id
    print('\n송신대상: ' + stc_id + "[" + stc_name + "]")

    return data


# 친구에게 메시지송신
def send_message_to_friends(data):
    # 토큰조회
    db_class = dbModule.Database()
    sql = "SELECT code, access_token from stock_search.kakao_token where msger_tcd = 'telegram'"
    row = db_class.executeOne(sql)

    telgm_token = row['access_token']
    chat_id = row['code']
    bot = telegram.Bot(token=telgm_token)

    bot.sendMessage(chat_id=chat_id, text=data) # -1001243985347, 1464479777:AAFhQAL7l7beuWbJivYbReXNEHqfePYlFr4
    print('친구에게 메시지를 성공적으로 보냈습니다.')
