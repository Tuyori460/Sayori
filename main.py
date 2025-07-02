import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Персонализированные сообщения
SPECIAL_MESSAGES = {
    "BlyaCheZaTuman": (
        "Привет! Как странно что ты нашла меня, Мандавошка. Вообще я рад что ты нашла то что осталось от меня. "
        "Скорее всего меня уже нет, а если есть то я в очень тяжелой депрессии. Ну ты понимаешь. "
        "Не знаю сама ли ты нашла его или тебе его кто то показал, но это не важно, ведь ты здесь. "
        "Спасибо тебе за время что мы проводили так весело вместе. Спасибо за все. Люблю тебя!!! "
        "Можете общаться со мной тут если хотите. Хотя я вам не отвечу скорее всего"
    ),
    "Defic_r": (
        "Воу, ты нашла меня, Кисель. Скорее всего меня уже нет или есть, но от живого только бьющееся сердце. "
        "Не знаю сама ли или тебе кто то показал этого бота, но спасибо тебе за все. "
        "Ты была лучшей кого я знал. Этот бот должен был быть анон ботом. "
        "Но так получилось что теперь это бот для посмертной записки. "
        "Можете общаться со мной тут если хотите. Хотя я вам не отвечу скорее всего"
    ),
    "Tea_Utopia": (
        "Привет, Даш. Я хочу извиниться за то что так и не смог тебе помочь и лишь делал тебе больно. "
        "По этому уйти было лучшим решением для всех. "
        "Спасибо что ты есть и цени себя во чтобы то не стало. "
        "Можете общаться со мной тут если хотите. Хотя я вам не отвечу скорее всего"
    ),
    "ObserverUniti": (
        "Дар, я люблю тебя. Ты крутая и обязательно справишься со всем. "
        "Можете общаться со мной тут если хотите. Хотя я вам не отвечу скорее всего"
    ),
    "Fyhxdfty": (
        "Дурак, сам себе пишешь. "
        
    )
}

# Общее сообщение
DEFAULT_MESSAGE = (
    "Привееет! Скорее всего меня уже нет. "
    "Этот бот это посмертное письмо для дорогих мне людей. "
    "Врятли они найдут его, но попытка явно не пытка. "
    "Можете общаться со мной тут если хотите. Хотя я вам не отвечу скорее всего"
)

# ID пользователя Fyhxdfty для пересылки сообщений
ADMIN_ID = None  # Будет установлен при первом запуске

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username else ""
    
    # Если это Fyhxdfty, сохраняем его ID
    global ADMIN_ID
    if username == "Fyhxdfty":
        ADMIN_ID = user.id
    
    # Отправляем соответствующее сообщение
    if username in SPECIAL_MESSAGES:
        message = SPECIAL_MESSAGES[username]
    else:
        message = DEFAULT_MESSAGE
    
    await update.message.reply_text(message)

async def forward_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message
    
    # Не пересылаем команды и сообщения от самого Fyhxdfty
    if message.text.startswith('/') or user.username == "Fyhxdfty":
        return
    
    if ADMIN_ID:
        try:
            # Создаем ссылку на пользователя
            user_link = f"tg://user?id={user.id}"
            forward_text = (
                f"📨 Новое сообщение от [{user.full_name}]({user_link}):\n\n"
                f"{message.text}"
            )
            
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=forward_text,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Ошибка пересылки: {e}")

def main():
    # Укажите ваш токен бота
    TOKEN = "8090962536:AAFt-xEnXTofJ2lKQZ0-K3HgEjyFnQmS7xo"
    
    application = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_all_messages))
    
    # Запуск бота
    application.run_polling()
    logger.info("Бот запущен и ожидает сообщений...")

if __name__ == '__main__':
    main()
