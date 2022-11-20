import telebot
from keys_config import keys
from token_config import BOT_TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в следующем формате:\n' \
           '<имя валюты, цену которой хотите узнать> \
           <имя валюты, в которой надо узнать цену первой валюты> \
           <количество первой валюты>\n ' \
           '<Для получения списка всех доступных валют введите команду /values >'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список всех доступных валют:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        input_array = message.text.split(' ')

        if len(input_array) != 3:
            raise APIException(f'Некорректное число параметров.')

        quote, base, amount = values
        sum = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    text = f'Итоговая цена: {sum}'
    bot.send_message(message.chat.id, text)


bot.polling()
