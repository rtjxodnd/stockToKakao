import telegram
token = '1464479777:AAFhQAL7l7beuWbJivYbReXNEHqfePYlFr4'
bot = telegram.Bot(token=token)

for i in bot.getUpdates():
    print(i.message)