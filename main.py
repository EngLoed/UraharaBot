import telebot
import os
import random
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest

load_dotenv()  # Загружает .env файл

# Создаем экземпляр бота
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# Функция для создания кнопки "Бросить кубик"
def create_dice_button():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Бросить кубик 🎲", callback_data="roll_dice")
    keyboard.add(button)
    return keyboard

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    welcome_text = (
        "Я на связи! 🎲\n\n"
        "Я автоматически принимаю запросы на вступление в канал и могу бросить кубик.\n"
        "Нажми кнопку ниже, чтобы бросить кубик!"
    )
    bot.send_message(m.chat.id, welcome_text, reply_markup=create_dice_button())

# Обработчик нажатия на кнопку "Бросить кубик"
@bot.callback_query_handler(func=lambda call: call.data == "roll_dice")
def handle_dice_callback(call):
    dice_roll = random.randint(1, 6)
    result_text = f"🎲 Выпало: {dice_roll}"
    
    # Редактируем сообщение с новым результатом
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=result_text,
        reply_markup=create_dice_button()
    )
    
    # Подтверждаем получение callback
    bot.answer_callback_query(call.id)

# Обработчик запросов на вступление в канал
@bot.chat_join_request_handler()
def handle_join_request(message: ChatJoinRequest):
    try:
        # Одобряем запрос на вступление
        bot.approve_chat_join_request(message.chat.id, message.from_user.id)
        
        # Отправляем приветственное сообщение пользователю
        welcome_message = (
            "🎉 Добро пожаловать! Ваш запрос на вступление одобрен.\n\n"
            "Напишите /start для начала работы с ботом."
        )
        bot.send_message(message.from_user.id, welcome_message)
        
    except Exception as e:
        print(f"Ошибка при обработке запроса на вступление: {e}")

# Получение сообщений от пользователя
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.lower() in ['кубик', 'dice', 'бросить', '🎲']:
        # Если пользователь написал ключевые слова - бросаем кубик
        dice_roll = random.randint(1, 6)
        result_text = f"🎲 Выпало: {dice_roll}"
        bot.send_message(message.chat.id, result_text, reply_markup=create_dice_button())
    else:
        # Стандартный ответ на другие сообщения
        response = (
            f"Вы написали: {message.text}\n\n"
            "Используйте /start для начала работы или нажмите кнопку 'Бросить кубик 🎲'"
        )
        bot.send_message(message.chat.id, response, reply_markup=create_dice_button())

# Запускаем бота
print("Бот запущен и готов к работе!")
bot.polling(none_stop=True, interval=0)
