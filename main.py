import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest
import random

# Токен бота
BOT_TOKEN = "8294445897:AAFI_EIWUQmmWoqB7JC-yjfF7wZiDZQzIuI"
bot = telebot.TeleBot(BOT_TOKEN)

# Создание кнопки
def create_dice_button():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Бросить кубик 🎲", callback_data="roll_dice")
    keyboard.add(button)
    return keyboard

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Нажми кнопку чтобы бросить кубик:",
        reply_markup=create_dice_button()
    )

# Обработка нажатия кнопки
@bot.callback_query_handler(func=lambda call: call.data == "roll_dice")
def dice_callback(call):
    dice_number = random.randint(1, 6)
    bot.edit_message_text(
        f"🎲 Выпало: {dice_number}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=create_dice_button()
    )
    bot.answer_callback_query(call.id)

# Автопринятие в канал
@bot.chat_join_request_handler()
def approve_join_request(message: ChatJoinRequest):
    try:
        bot.approve_chat_join_request(message.chat.id, message.from_user.id)
        bot.send_message(
            message.from_user.id,
            "✅ Ваш запрос на вступление одобрен! Напишите /start для начала работы."
        )
    except Exception as e:
        print(f"Ошибка: {e}")

# Запуск бота
print("Бот запущен!")
bot.infinity_polling()

if __name__ == '__main__':
    main()
