import asyncio
import logging
from telegram.ext import (
    Application,
    ChatJoinRequestHandler,
    CommandHandler,
    ContextTypes,
)
from telegram import Update

# ===============================================
#   НАСТРОЙКИ — ИЗМЕНИ ЭТО ПОД СЕБЯ
# ===============================================

BOT_TOKEN = "8702681196:AAGHWA8ZBjvuWMCUtAlJxbPWQozOvFwHrGg"       # токен от @BotFather
CHANNEL_ID = -7104850094          # ID твоего закрытого канала (со знаком минус!)

# ===============================================
#   ТЕКСТЫ СООБЩЕНИЙ
# ===============================================

# ДЕНЬ 1 — Сообщение 1 (сразу после заявки)
MESSAGE_1 = """Hey 👋

You've just requested access to my private channel — Henry Backman Trade.

While you're waiting for approval, you don't have to miss anything — I can already send you a live signal right now."""

# ДЕНЬ 1 — Сообщение 2 (сразу за сообщением 1, через 5 секунд)
MESSAGE_2 = """🔥 While you're waiting for approval, get the signal now:

👉 @Henry_CryptoBoss"""

# ДЕНЬ 1 — Сообщение 3 (через 2.5 часа)
MESSAGE_3 = """Did you already get in on a signal?

I'm preparing another setup right now. If you're here — you can still catch it before it goes public.

Text me 👇
👉 @Henry_CryptoBoss"""

# ДЕНЬ 2 (через 24 часа)
MESSAGE_4 = """Yesterday was a strong profit session 📈

Those who didn't wait and reached out early already locked in gains.

If you're ready for the next move — message me now:
👉 @Henry_CryptoBoss"""

# ДЕНЬ 3 (через 48 часов)
MESSAGE_5 = """Quick question —

Are you here just to watch, or to actually make money?

I only work with people who take action.

If you're serious, message me now and I'll send you the next entry:
👉 @Henry_CryptoBoss"""

# ===============================================
#   КОД БОТА — МЕНЯТЬ НЕ НУЖНО
# ===============================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def send_delayed_message(bot, user_id: int, text: str, delay_seconds: int):
    """Отправляет сообщение с задержкой"""
    await asyncio.sleep(delay_seconds)
    try:
        await bot.send_message(
            chat_id=user_id,
            text=text
        )
        logger.info(f"✅ Сообщение отправлено пользователю {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки пользователю {user_id}: {e}")


async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Срабатывает когда кто-то подаёт заявку на вступление в канал"""

    join_request = update.chat_join_request
    user = join_request.from_user
    chat = join_request.chat

    # Проверяем что заявка именно в наш канал
    if chat.id != CHANNEL_ID:
        return

    user_id = user.id
    first_name = user.first_name or "there"

    logger.info(f"📩 Новая заявка от {first_name} (ID: {user_id})")

    # Одобряем заявку автоматически
    try:
        await join_request.approve()
        logger.info(f"✅ Заявка пользователя {user_id} одобрена")
    except Exception as e:
        logger.error(f"❌ Не удалось одобрить заявку {user_id}: {e}")
        return

    # --- ДЕНЬ 1 ---

    # Сообщение 1 — сразу
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=MESSAGE_1
        )
    except Exception as e:
        logger.error(f"❌ Ошибка отправки сообщения 1 пользователю {user_id}: {e}")
        return

    # Сообщение 2 — через 5 секунд (сразу за первым)
    asyncio.create_task(
        send_delayed_message(context.bot, user_id, MESSAGE_2, delay_seconds=5)
    )

    # Сообщение 3 — через 2.5 часа (9000 секунд)
    asyncio.create_task(
        send_delayed_message(context.bot, user_id, MESSAGE_3, delay_seconds=9000)
    )

    # --- ДЕНЬ 2 --- через 24 часа (86400 секунд)
    asyncio.create_task(
        send_delayed_message(context.bot, user_id, MESSAGE_4, delay_seconds=86400)
    )

    # --- ДЕНЬ 3 --- через 48 часов (172800 секунд)
    asyncio.create_task(
        send_delayed_message(context.bot, user_id, MESSAGE_5, delay_seconds=172800)
    )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start — если кто-то написал боту напрямую"""
    await update.message.reply_text(
        "👋 This bot works automatically.\n\n"
        "Submit a join request to the channel and I'll message you right away!"
    )


def main():
    """Запуск бота"""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(ChatJoinRequestHandler(handle_join_request))

    logger.info("🚀 Бот запущен и ждёт заявок...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
