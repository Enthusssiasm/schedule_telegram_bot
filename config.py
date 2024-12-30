import os
from dotenv import load_dotenv
from pytz import timezone
from logging_config import setup_logger

logger = setup_logger()

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN не найден в .env файле")
    raise ValueError("BOT_TOKEN не найден в .env файле")

YEKATERINBURG_TZ = timezone('Asia/Yekaterinburg')
MOSCOW_TZ = timezone('Europe/Moscow')
LONDON_TZ = timezone('Europe/London')
NEW_YORK_TZ = timezone('America/New_York')
LOS_ANGELES_TZ = timezone('America/Los_Angeles')
BERLIN_TZ = timezone('Europe/Berlin')
TOKYO_TZ = timezone('Asia/Tokyo')
BEIJING_TZ = timezone('Asia/Shanghai')
SYDNEY_TZ = timezone('Australia/Sydney')