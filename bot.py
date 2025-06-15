from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

GROUP_CHAT_ID = -4735051058

user_orders = {}

main_menu = ReplyKeyboardMarkup(
    [["👟 Кроссовки", "🧥 Одежда", "🕶 Аксессуары"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 Добро пожаловать в *GIREX*!\n\n"
        "Мы предлагаем только топовые кроссовки, одежду и аксессуары.\n\n"
        "Выберите категорию ниже, чтобы оформить заказ:",
        reply_markup=main_menu,
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id

    if text in ["👟 Кроссовки", "🧥 Одежда", "🕶 Аксессуары"]:
        user_orders[chat_id] = {"category": text}
        await update.message.reply_text("✏️ Введите название модели:")
    elif chat_id in user_orders and "model" not in user_orders[chat_id]:
        user_orders[chat_id]["model"] = text
        await update.message.reply_text("📏 Укажите размер:")
    elif chat_id in user_orders and "size" not in user_orders[chat_id]:
        user_orders[chat_id]["size"] = text
        await update.message.reply_text("🙍 Ваше имя:")
    elif chat_id in user_orders and "name" not in user_orders[chat_id]:
        user_orders[chat_id]["name"] = text
        await update.message.reply_text("🏙 Город:")
    elif chat_id in user_orders and "city" not in user_orders[chat_id]:
        user_orders[chat_id]["city"] = text
        await update.message.reply_text("📱 Телефон или @никнейм:")
    elif chat_id in user_orders and "contact" not in user_orders[chat_id]:
        user_orders[chat_id]["contact"] = text

        order = user_orders[chat_id]
        message = (
            "📥 *Новый заказ GIREX:*\n\n"
            f"🛍 Категория: {order['category']}\n"
            f"📦 Модель: {order['model']}\n"
            f"📐 Размер: {order['size']}\n"
            f"🙋 Имя: {order['name']}\n"
            f"🏙 Город: {order['city']}\n"
            f"📞 Контакт: {order['contact']}"
        )

        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode="Markdown")
        await update.message.reply_text("✅ Ваш заказ отправлен! Менеджер скоро с вами свяжется.")
        del user_orders[chat_id]
    else:
        await update.message.reply_text("❗ Пожалуйста, начните с выбора категории — нажмите /start")

def main():
    app = ApplicationBuilder().token("8178477896:AAFElDDVQFdmU3ovXBeSR4VygtTRlhhyV6Y").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == "__main__":
    main()
