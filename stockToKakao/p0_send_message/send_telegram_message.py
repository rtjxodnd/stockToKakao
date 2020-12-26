import telegram
telgm_token = '1464479777:AAFhQAL7l7beuWbJivYbReXNEHqfePYlFr4'
bot = telegram.Bot(token=telgm_token)
updates = bot.getUpdates()
print(updates)
for i in updates:
    print(i)

print('start telegram chat bot')