# import telegram
# telgm_token = '1464479777:AAFhQAL7l7beuWbJivYbReXNEHqfePYlFr4'
# bot = telegram.Bot(token=telgm_token)
# bot.sendMessage(chat_id = '-1001243985347', text="챗봇 테스트")
#
#

# updates = bot.getUpdates()
# print(updates)
# for i in updates:
#     print(i)
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from stockToKakao.commonModule import telegramModule
print('start telegram chat bot')

msg = telegramModule.set_data('005930', '삼성전자', '한번 쭈우우욱 가즈아~~~!!!')
telegramModule.send_message_to_friends(msg)
