from telegram import Update
from telegram.ext import ContextTypes
from utils import generate_password
from schedule_operations import get_schedule, get_tomorrow_schedule, send_schedule, send_tomorrow_schedule
from logging_config import setup_logger
from db_operations import add_user, delete_user
from config import YEKATERINBURG_TZ
from datetime import time


logger = setup_logger()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений."""
    text = update.message.text
    user_id = update.effective_user.id
    logger.info(f"Сообщение от пользователя {user_id}: {text}")

    if text == "🔒 Сгенерировать пароль":
        password = generate_password()
        await update.message.reply_text(f"Ваш случайный пароль: {password}")
    elif text == "🙄 Расписание на сегодня":
        schedule = get_schedule()
        await update.message.reply_text(schedule, parse_mode='HTML')
    elif text == "😯 К чему готовиться завтра?":
        tomorrow_schedule = get_tomorrow_schedule()
        await update.message.reply_text(tomorrow_schedule, parse_mode='HTML')
    elif text == "🧩 Узнать больше":
        await update.message.reply_text("Привет! Я могу помочь с паролями и расписанием.")
    elif text == "📣 Подписаться на рассылку":
        is_new_user = add_user(user_id)

        if is_new_user:
            context.job_queue.run_daily(
                send_schedule, 
                time=time(8, 0, tzinfo=YEKATERINBURG_TZ), 
                chat_id=int(user_id), 
                name=f"schedule_{user_id}"
            )
            context.job_queue.run_daily(
                send_tomorrow_schedule, 
                time=time(22, 0, tzinfo=YEKATERINBURG_TZ), 
                chat_id=int(user_id), 
                name=f"tomorrow_schedule_{user_id}"
            )
            await update.message.reply_text("Вы подписались на рассылку расписания (Каждый день в 8:00 и 22:00).")
        else:
            await update.message.reply_text("Вы уже подписаны на рассылку.")
    elif text == "❌ Отписаться от рассылки":
        is_deleted_user = delete_user(user_id)
        if is_deleted_user:
            # Удаляем задачу из job_queue
            for name in [f"schedule_{user_id}", f"tomorrow_schedule_{user_id}"]:
                current_jobs = context.job_queue.get_jobs_by_name(name)
                for job in current_jobs:
                    job.schedule_removal()
            await update.message.reply_text("Вы отписались от рассылки.")
        else:
            await update.message.reply_text("Вы не подписаны на рассылку.")
    else:
        await update.message.reply_text(f"{text}")