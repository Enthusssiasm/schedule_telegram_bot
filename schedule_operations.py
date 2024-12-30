from logging_config import setup_logger
from datetime import datetime, timedelta
from weeks import WEEK1, WEEK2
from telegram.ext import CallbackContext

logger = setup_logger()


def get_schedule():
    """Возвращает расписание на сегодня."""
    today = datetime.now()
    day_of_week = today.weekday()  # Понедельник = 0, Воскресенье = 6
    week_number = today.isocalendar()[1] % 2  # Чётность недели (1-я или 2-я)
    
    logger.info(f"Расписание запрошено для дня {day_of_week} и недели {week_number}")
    if day_of_week >= len(WEEK1):
        return "Сегодня нет занятий :)"
    return WEEK1[day_of_week] if week_number == 1 else WEEK2[day_of_week]

async def send_schedule(context: CallbackContext):
    """Отправляет расписание подписчикам."""
    chat_id = context.job.chat_id
    schedule = get_schedule()
    await context.bot.send_message(chat_id, text=schedule, parse_mode='HTML')
    logger.info(f"Отправлено расписание пользователю {chat_id}")

def get_tomorrow_schedule():
    """Возвращает расписание на завтра."""
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    day_of_week = tomorrow.weekday()  # Понедельник = 0, Воскресенье = 6
    week_number = tomorrow.isocalendar()[1] % 2  # Чётность недели (1-я или 2-я)
    
    logger.info(f"Расписание на завтра запрошено для дня {day_of_week} и недели {week_number}")
    if day_of_week >= len(WEEK1):  # Если завтра воскресенье
        return "Завтра нет занятий :)"
    return WEEK1[day_of_week] if week_number == 1 else WEEK2[day_of_week]

async def send_tomorrow_schedule(context: CallbackContext):
    """Отправляет расписание на завтра подписчикам."""
    chat_id = context.job.chat_id
    schedule = get_tomorrow_schedule()
    await context.bot.send_message(chat_id, text=f"Расписание на завтра:\n\n{schedule}", parse_mode='HTML')
    logger.info(f"Отправлено расписание на завтра пользователю {chat_id}")