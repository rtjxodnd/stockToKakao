import telegram
telgm_token = '1464479777:AAFhQAL7l7beuWbJivYbReXNEHqfePYlFr4'
bot = telegram.Bot(token=telgm_token)


bot.sendMessage(chat_id = '-1001243985347', text="챗봇 테스트")



# updates = bot.getUpdates()
# print(updates)
# for i in updates:
#     print(i)

print('start telegram chat bot')