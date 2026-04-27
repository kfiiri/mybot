import asyncio
import logging
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, CommandHandler, ContextTypes

# ===============================================
#   НАСТРОЙКИ — ИЗМЕНИ ЭТО ПОД СЕБЯ
# ===============================================

BOT_TOKEN = "8702681196:AAGhWA8ZBjvuWMCUtAlJxbPWQozOvFwHrGg"
CHANNEL_ID = -1002437555732

# ===============================================
#   ТЕКСТЫ СООБЩЕНИЙ
# ===============================================

MESSAGE_1 = """Hey 👋

You've just requested access to my private channel — Henry Backman Trade.

While you're waiting for approval, you don't have to miss anything — I can already send you a live signal right now."""

MESSAGE_2 = """🔥 While you're waiting for approval, get the signal now:

👉 @Henry_CryptoBoss"""

MESSAGE_3 = """Did you already get in on a signal?

I'm preparing another setup right now. If you're here — you can still catch it before it goes public.

Text me 👇
👉 @Henry_CryptoBoss"""

MESSAGE_4 = """Yesterday was a strong profit session 📈

Those who didn't wait and reached out early already locked in gains.

If you're ready for the next move — message me now:
👉 @Henry_CryptoBoss"""

MESSAGE_5 = """Quick question —

Are you here just to watch, or to actually make money?

I only work with people who take action.

If you're serious, message me now and I'll send you the next entry:
👉 @Henry_CryptoBoss"""

# ===============================================
#   КОД БОТА
# ===============================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def send_delayed(bot, user_id: int, text: str, delay: int):
    await asyncio.sleep(delay)
    try:
        await bot.send_message(chat_id=user_id, text=text)
        logger.info(f"✅ Сообщение отправлено {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка {user_id}: {e}")


async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    join_request = update.chat_join_request
    user = join_request.from_user
    chat = join_request.chat

    if chat.id != CHANNEL_ID:
        return

    user_id = user.id
    logger.info(f"📩 Заявка от {user.first_name} (ID: {user_id})")

    try:
        await join_request.approve()
        logger.info(f"✅ Заявка одобрена {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка одобрения {user_id}: {e}")
        return

    try:
        await context.bot.send_message(chat_id=user_id, text=MESSAGE_1)
    except Exception as e:
        logger.error(f"❌ Не могу написать {user_id}: {e}")
        return

    asyncio.create_task(send_delayed(context.bot, user_id, MESSAGE_2, 5))
    asyncio.create_task(send_delayed(context.bot, user_id, MESSAGE_3, 9000))
    asyncio.create_task(send_delayed(context.bot, user_id, MESSAGE_4, 86400))
    asyncio.create_task(send_delayed(context.bot, user_id, MESSAGE_5, 172800))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 This bot works automatically.\n\nSubmit a join request to the channel and I'll message you!"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    logger.info("🚀 Бот запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
