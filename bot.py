import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from database.db import init_db
from handlers.commands import (
    ayuda,
    escribirAtodos,
    guardaruser,
    mostrarusuarios,
    start,
    tuinfo,
)

load_dotenv()
init_db()
TOKEN = os.getenv("TOKEN")

        
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("guardaruser", guardaruser))
app.add_handler(CommandHandler("tuinfo", tuinfo))
app.add_handler(CommandHandler("escribirAtodos", escribirAtodos))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ayuda", ayuda))
app.add_handler(CommandHandler("mostrarusuarios", mostrarusuarios))
    # app.add_handler(
    #     MessageHandler(
    #         filters.TEXT & ~filters.COMMAND,
    #         reply
    #     )
    # )

print("Bot iniciado...")

app.run_polling()