from telegram.ext import Application, CommandHandler

# Функция обработчика для команды /start
async def start(update, context):
    await update.message.reply_text("Бот запущен и готов к работе!")

def main():
    # Создаём объект Application с вашим токеном
    application = Application.builder().token("7851649387:AAE0ovMqW7U3WFL6pCetd3aQLMwoJptuKwo").build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()