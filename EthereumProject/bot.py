import telebot
from telebot import types
from telebot import apihelper
import requests
from datetime import datetime
from pycbrf.toolbox import ExchangeRates
import time

TOKEN = '817147179:AAEtC2bKJyxTeWsEgE2uM028hS_cOdCAtF0'
bot = telebot.TeleBot(TOKEN)
arr = ['BTC']
arr2 = ['']


def setup_proxy():
    apihelper.proxy = {'https': 'https://165.22.32.197:8118'}


def update_DB(array, name):
    db = open('Database/' + name + '.txt', 'w+')
    for i in range(len(array)):
        db.write(str(array[i]))


@bot.message_handler(func=lambda message: True)
def send_all(message):
    chat_id = message.chat.id
    name = message.from_user.username
    update_DB(arr, name)
    if message.text == '/start' or message.text == '/help' or message.text == '/info' \
            or message.text == '/add_currency' or message.text == '/remove_currency':
        if message.text == '/help':
            bot.send_message(chat_id,
                             '/info - для получения информации о курсах криптовалюты, которую вы внесли в список'
                             + '\n' + '/add_currency - для добавления криптовалюты в список, '
                                      'которую вы хотите отслеживать'
                             + '\n' + '/remove_currency - для удаления криптовалюты из списка,'
                                      ' которую вы не хотите отслеживать')
        elif message.text == '/start':
            bot.send_message(chat_id, 'Здравствуйте, я ваш помошник в мире криптовалюты.' + '\n'
                             + 'Мой создатель - Арутюнян Андрей. 15 лет.' + '\n' + 'Сидит на компом 24/7 и дорабатывает'
                                ' меня.' + '\n'
                             + 'Если нужна помощь - команда /help')
            while True:
                if str(datetime.now().strftime(format='%H')) == '10':
                    send(chat_id)
                    break
                elif str(datetime.now().strftime(format='%H')) == '14':
                    send(chat_id)
                    break
                elif str(datetime.now().strftime(format='%H')) == '19':
                    send(chat_id)
                    break
        elif message.text == '/info':
            send(chat_id, message)
            bot.send_message(chat_id, 'В данный момент курс отслеживаемых вами валют буду отправлены вам в 10:00, '
                                      '14:00, 19:00.' + '\n' +
                             'Изменения этого времени сделаю в будущем обновлении.')
        elif message.text == '/add_currency':
            bot.send_message(chat_id, 'Введите название криптовалюты, которую вы хотите добавить в вам список' + '\n'
                             + 'Пример: BTC')
            arr2[0] = 'add'
        elif message.text == '/remove_currency':
            bot.send_message(chat_id, 'Введите название криптовалюты, которую вы хотите удалить из вашего списка' + '\n'
                             + 'Пример: BTC')
            arr2[0] = 'remove'
    else:
        i = 0
        for i2 in range(len(arr)):
            if arr2[0] == 'remove':
                if arr[i] == message.text:
                    arr.remove(message.text)
                    update_DB(arr, name)
                    bot.send_message(chat_id,
                                     'Криптовалюта успешно удалена из вашего списка!' + '\n' + 'Ваш список: ' + str(
                                         arr))
                    break
                else:
                    bot.send_message(chat_id, 'Этой валюты нет в вашем списке!')
                    break
            if arr2[0] == 'add':
                if arr[i] != message.text:
                    try:
                        currency_url = 'https://yobit.net/api/2/' + str(message.text.lower()) + '_usd/ticker'
                        currency_response = requests.get(currency_url).json()
                        currency_dollars = float(currency_response['ticker']['last'])
                        arr.append(message.text)
                        update_DB(arr, name)
                        bot.send_message(chat_id,
                                         'Криптовалюта успешно добавлена в вам список!' + '\n' + 'Ваш список: ' + str(
                                             arr))
                    except:
                        bot.send_message(chat_id, message.text + ' - Такой валюты не существует!')

                    break
                else:
                    bot.send_message(chat_id, 'Эта валюта уже есть в вашем списке!')
                    break
            i += 1


def get_currency(currency):
    currency_url = 'https://yobit.net/api/2/' + str(currency.lower()) + '_usd/ticker'
    currency_response = requests.get(currency_url).json()
    currency_dollars = float(currency_response['ticker']['last'])
    return currency_dollars


def get_usd():
    rates = ExchangeRates(datetime.now().date())
    usd_rub = float(rates['USD'].value)
    return usd_rub


def setup_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    info_item = types.KeyboardButton('/info')
    help_item = types.KeyboardButton('/help')
    add_currency_item = types.KeyboardButton('/add_currency')
    remove_currency_item = types.KeyboardButton('/remove_currency')
    markup.add(info_item, help_item, add_currency_item, remove_currency_item)
    return markup

def send(chat_id, message):
    array = open('Database/' + message.from_user.username + '.txt', 'r+')
    array = list(array)
    i = 0
    for i2 in range(len(arr)):
        i += 1
        bot.send_message(chat_id, 'Date: ' + str(datetime.now().date()) + '\n' + 'Time: ' +
                                str(datetime.now().strftime(format='%H:%M:%S')) + '\n' + array[i - 1] + ': ' +
                                str(int(get_currency(array[i - 1]) * get_usd())) + ' RUB', reply_markup=setup_buttons())


setup_proxy()
setup_buttons()
try:
    bot.polling(none_stop=True)
except Exception as e:
    time.sleep(2)
