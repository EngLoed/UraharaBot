import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ChatJoinRequestHandler
import random

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота (замените на ваш токен)
BOT_TOKEN = "8294445897:AAFI_EIWUQmmWoqB7JC-yjfF7wZiDZQzIuI"

# ID канала (замените на ID вашего канала)
CHANNEL_ID = "-1002942039707"  # или -1001234567890 для приватных каналов

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("Бросить кубик 🎲", callback_data='roll_dice')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Привет! Я бот с функцией автопринятия в канал и игрой в кости.\n\n"
        "Нажми кнопку ниже, чтобы бросить кубик!",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'roll_dice':
        # Генерируем случайное число от 1 до 6
        dice_roll = random.randint(1, 6)
        await query.edit_message_text(
            text=f"🎲 Выпало: {dice_roll}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Бросить кубик 🎲", callback_data='roll_dice')]])
        )

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик запросов на вступление в канал"""
    chat_join_request = update.chat_join_request
    user_id = chat_join_request.from_user.id
    chat_id = chat_join_request.chat.id
    
    try:
        # Одобряем запрос на вступление
        await context.bot.approve_chat_join_request(chat_id, user_id)
        logger.info(f"Запрос на вступление одобрен для пользователя {user_id} в канал {chat_id}")
        
        # Отправляем приветственное сообщение пользователю
        await context.bot.send_message(
            chat_id=user_id,
            text="🎉 Добро пожаловать в наш канал! Ваш запрос на вступление был одобрен автоматически.\n\n"
                 "Вы можете использовать команду /start для начала работы с ботом."
        )
        
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса на вступление: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    keyboard = [
        [InlineKeyboardButton("Бросить кубик 🎲", callback_data='roll_dice')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/help - показать эту справку\n"
        "/dice - бросить кубик\n\n"
        "Бот автоматически одобряет запросы на вступление в канал.",
        reply_markup=reply_markup
    )

async def dice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /dice"""
    # Генерируем случайное число от 1 до 6
    dice_roll = random.randint(1, 6)
    keyboard = [
        [InlineKeyboardButton("Бросить кубик 🎲", callback_data='roll_dice')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🎲 Выпало: {dice_roll}",
        reply_markup=reply_markup
    )

def main():
    """Основная функция для запуска бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dice", dice_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(ChatJoinRequestHandler(handle_join_request))
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
