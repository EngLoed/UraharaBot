import telebot
import os
from dotenv import load_dotenv

load_dotenv()  # Загружает .env файл

# Создаем экземпляр бота
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# Обработчик запросов на вступление в канал
@bot.chat_join_request_handler()
def handle_join_request(message):
    try:
        # Одобряем запрос на вступление
        bot.approve_chat_join_request(message.chat.id, message.from_user.id)
        
        # Отправляем сообщение пользователю
        bot.send_message(
            message.from_user.id, 
            "✅ Ваша заявка на вступление в канал одобрена! Добро пожаловать!"
        )
        
    except Exception as e:
        print(f"Ошибка: {e}")

# Запускаем бота
bot.polling(none_stop=True, interval=0)
