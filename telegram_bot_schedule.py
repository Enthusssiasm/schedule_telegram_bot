from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CommandHandler, Application, MessageHandler, filters, ContextTypes
from datetime import time
from config import BOT_TOKEN, YEKATERINBURG_TZ
from logging_config import setup_logger
from db_operations import get_all_users
from schedule_operations import send_schedule, send_tomorrow_schedule
from bot_keyboard import handle_message

logger = setup_logger()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start."""
    logger.info(f"Получена команда /start от пользователя {update.effective_user.id}")
    keyboard = [
        ["🔒 Сгенерировать пароль", "🙄 Расписание на сегодня"],
        ["😯 К чему готовиться завтра?", "🧩 Узнать больше"],
        ["📣 Подписаться на рассылку", "❌ Отписаться от рассылки"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите действие..."
    )
    await update.message.reply_text(
        'Привет! Я могу генерировать случайный пароль, а также отправлять расписание занятий :)',
        reply_markup=reply_markup
    )

def main():
    """Основная функция запуска бота."""
    logger.info("Запуск бота.")
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        # После перезагрузки бота восстановление задач рассылки
        all_users = get_all_users()
        for user_id in all_users:
            application.job_queue.run_daily(
                send_schedule, 
                time=time(8, 0, tzinfo=YEKATERINBURG_TZ),
                chat_id=int(user_id),
                name=f"schedule_{user_id}"
            )
            application.job_queue.run_daily(
                send_tomorrow_schedule, 
                time=time(22, 0, tzinfo=YEKATERINBURG_TZ), 
                chat_id=int(user_id), 
                name=f"tomorrow_schedule_{user_id}"
            )
            logger.info(f"Задача рассылки восстановлена для пользователя {user_id}")

        application.add_handler(CommandHandler('start', start_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.run_polling()
    except Exception as e:
        logger.error(f"Ошибка в приложении: {e}")
        raise

if __name__ == "__main__":
    main()