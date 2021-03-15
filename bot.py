import telebot
from telebot import types
import requests
from requests_toolbelt import MultipartEncoder
from bs4 import BeautifulSoup
import urllib.request
import json
import os

_token_bot = telebot.TeleBot('') #токен


@_token_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "💥Из рекомендаций💥":
        head = {'User-Agent': 'Mozilla/5.0'}

        post = requests.get('https://www.tiktok.com/?lang=ru-RU', headers=head)

        soup = BeautifulSoup(post.content, "html.parser")
        for link in soup.findAll('a'):
            print(link.get('href'))

        _token_bot.send_message(message.chat.id, "Попозже :(")

    if message.text == "🌅Клипы🌅":
        cwd = os.getcwd()
        if not os.path.isfile(fr"{cwd}\tokens\{message.from_user.id}.txt"):
            return _token_bot.send_message(message.chat.id, "⚠У тебя отсутствует токен!⚠\n"
                                                            "Поставить его можно в настройках.")
        mm = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button1 = types.KeyboardButton("💫По URL💫")
        button2 = types.KeyboardButton("💥Из рекомендаций💥")
        button3 = types.KeyboardButton("👣Назад👣")
        mm.add(button1, button2, button3)

        _token_bot.send_message(message.chat.id, "⚠Выбери режим который тебе нравится!\n\n"
                                                 "✅По URL - загрузка видео по ссылке.\n"
                                                 "🚫Из рекомендаций - загрузка видео из реком. в автоматическом режиме",
                                reply_markup=mm)

    if message.text == "/start" or message.text == "👣Назад👣":
        mm = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button1 = types.KeyboardButton("🌅Клипы🌅")
        button2 = types.KeyboardButton("📝Настройки📝")
        mm.add(button1, button2)

        _token_bot.send_message(message.chat.id, "Привет!", reply_markup=mm)

    if message.text == "📝Настройки📝":
        mm = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button1 = types.KeyboardButton("👣Назад👣")
        mm.add(button1)

        msg = _token_bot.send_message(message.chat.id, "👥Для работы бота необходим твой токен ВКонтакте👥\n\n"
                                                       "Добыть токен можно на сайте: vkhost.github.io/\n"
                                                       "Необходимо выбрать VK Me, нажать разрешить и скопировать часть адресной строки от access_token= до &expires_in\n\n"
                                                       "✅Далее просто отправьте токен боту, он его сохранит✅",
                                      reply_markup=mm)

        _token_bot.register_next_step_handler(msg, _create_token)

    if message.text == "💫По URL💫" or message.text == "💫Загрузить💫":
        cwd = os.getcwd()
        if not os.path.isfile(fr"{cwd}\tokens\{message.from_user.id}.txt"):
            return _token_bot.send_message(message.chat.id, "⚠У тебя отсутствует токен!⚠\n"
                                                            "Поставить его можно в настройках.")
        msg = _token_bot.send_message(message.chat.id, "🗯Пожалуйста отправь мне ссылку на видео в TikTok🗯\n\n"
                                                       "⚠Пример:⚠\n"
                                                       "https://vt.tiktok.com/khpq9t/\n"
                                                       "https://www.tiktok.com/@philandmore/video/6805867805452324102\n\n"
                                                       "И другие.")

        _token_bot.register_next_step_handler(msg, _search_url)


def _search_url(message):
    if message.text == "👣Назад👣":
        mm = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button1 = types.KeyboardButton("🌅Клипы🌅")
        button2 = types.KeyboardButton("📝Настройки📝")
        mm.add(button1, button2)

        return _token_bot.send_message(message.chat.id, "Привет!", reply_markup=mm)

    _load_snaptik(message.text, message)


def _upload_to_vk(message):
    cwd = os.getcwd()
    token = open(fr"{cwd}\tokens\{message.from_user.id}.txt", "r")
    _upload_video(*token, message.text, message)


def _token_valid(token):
    data = {
        'access_token': token,
        'v': '5.123',
    }
    headers = {
        'key': 'users.get',
        'value': '5.123'
    }

    r = requests.post('https://api.vk.com/method/users.get', data=data, headers=headers)
    try:
        upload_url = r.json()['error']['error_code']
        return 0
    except KeyError:
        return 1


def _create_token(message):
    if message.text == "":
        return _token_bot.send_message(message.chat.id, "⚠Нельзя отправлять пустую строку!⚠")
    if message.text == "👣Назад👣":
        mm = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button1 = types.KeyboardButton("🌅Клипы🌅")
        button2 = types.KeyboardButton("📝Настройки📝")
        mm.add(button1, button2)

        return _token_bot.send_message(message.chat.id, "Привет!", reply_markup=mm)

    if _token_valid(message.text) == 0:
        msg = _token_bot.send_message(message.chat.id, "⚠Данный токен недействителен! Введите токен еще раз.⚠")
        return _token_bot.register_next_step_handler(msg, _create_token)

    cwd = os.getcwd()

    my_file = open(fr"{cwd}\tokens\{message.from_user.id}.txt", "w+")
    my_file.write(message.text)
    my_file.close()

    _token_bot.send_message(message.chat.id, "✅Отлично! Я запомнил твой токен✅")


def _load_snaptik(lin, message):
    if message.text == "👣Назад👣":
        mm = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button1 = types.KeyboardButton("🌅Клипы🌅")
        button2 = types.KeyboardButton("📝Настройки📝")
        mm.add(button1, button2)

        _token_bot.send_message(message.chat.id, "Привет!", reply_markup=mm)

    cwd = os.getcwd()
    if os.path.isfile(fr'{cwd}\video.mp4'):
        os.remove(fr'{cwd}\video.mp4')

    url = 0
    head = {'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7CwxCXhJ7UIYYnji',
            'Cookie': 'PHPSESSID=sf89oogdslb85de7ec42j4mgl3; current_language=ru'}

    requests.post('https://snaptik.app/check_token.php', headers=head,
                  data=MultipartEncoder(fields={}, boundary='----WebKitFormBoundary7CwxCXhJ7UIYYnji'))

    dat = MultipartEncoder(fields={'url': lin},
                           boundary='----WebKitFormBoundary7CwxCXhJ7UIYYnji')
    post = requests.post('https://snaptik.app/action_2021.php', headers=head, data=dat)

    soup = BeautifulSoup(post.content, "html.parser")
    for link in soup.findAll('a'):
        url = link.get('href')
        break

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    try:
        urllib.request.urlretrieve(url, 'video.mp4')
    except TypeError:
        msg = _token_bot.send_message(message.chat.id, "⚠Данная ссылка недействительна, введите другую.⚠")
        return _token_bot.register_next_step_handler(msg, _search_url)

    msg = _token_bot.send_message(message.chat.id, "✅Клип успешно загружен, придумай описание:✅")
    _token_bot.register_next_step_handler(msg, _upload_to_vk)


def _upload_video(token, title, message):
    size = os.path.getsize('video.mp4')
    data = {
        'access_token': token,
        'v': '5.123',
        'file_size': size,
        'description': title,
        'title': title
    }
    headers = {
        'key': 'shortVideo.create',
        'value': '5.123'
    }

    r = requests.post('https://api.vk.com/method/shortVideo.create', data=data, headers=headers)
    upload_url = r.json()['response']['upload_url']

    my_file = open('video.mp4', 'rb')
    up = {'video': ('6902784884750814465.mp4', my_file, "multipart/form-data")}

    requests.post(upload_url, files=up)

    mm = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton("💫Загрузить💫")
    button2 = types.KeyboardButton("👣Назад👣")
    mm.add(button1, button2)

    _token_bot.send_message(message.chat.id, "✅Клип успешно загружен! Повторим?✅",
                            reply_markup=mm)


_token_bot.polling(none_stop=True, interval=0)
