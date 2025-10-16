import telebot
import threading
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot("TOKEN")

# Кнопки для выбора времени
def alarm_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("10 секунд"),
        KeyboardButton("20 секунд"),
        KeyboardButton("30 секунд")
    )
    return keyboard


# При /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Выбери, через сколько секунд разбудить тебя:",
        reply_markup=alarm_keyboard()
    )

# Обработчик выбора времени
@bot.message_handler(func=lambda message: message.text in ["10 секунд", "20 секунд", "30 секунд"])
def set_alarm(message):
    delay_map = {
        "10 секунд": 10,
        "20 секунд": 20,
        "30 секунд": 30
    }
    delay = delay_map[message.text]
    bot.reply_to(message, f"Будильник поставлен на {delay} секунд ⏳")

    # Стартуем таймер в отдельном потоке
    threading.Timer(delay, send_alarm, args=[message.chat.id]).start()

# Что делать, когда время вышло
def send_alarm(chat_id):
    bot.send_message(chat_id, "⏰ Время вышло! Просыпайся!")

# Запуск бота
bot.polling()
