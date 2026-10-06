from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Helloworld."
    )
async def ayuda (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "estos son mis comantos \n"
        "/start \n"
        "inicia el bot \n"
        "/ayuda \n"
        "muestra este mensaje \n"
        "/tuinfo \n"
        "muestra tu informacion \n"
        "/guardaruser \n"
        "guarda tu id de usuario \n"
        "/mostrarusuarios \n"
        "muestra los usuarios guardados \n"
        "/escribirAtodos \n"
        "escribe a todos los usuarios \n"
        
    )
async def reply(update, context):
    texto = update.message.text

    await update.message.reply_text(
        f'tu mensaje:\n{texto}'
    )
async def tuinfo(update, context): 
    usuario = update.effective_user
    await update.message.reply_text(
        "esta es tu info \n"
        f'{usuario.id}\n {usuario.first_name} \n {usuario.username}'
    )
usuarios = []
async def guardaruser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "usuario guardado")
    usuario = update.effective_user
    usuarios.append(usuario.id)

async def mostrarusuarios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if usuarios:
        await update.message.reply_text(
            "Usuarios guardados:\n" + "\n".join(str(user_id) for user_id in usuarios)
        )
    else:
        await update.message.reply_text("No hay usuarios guardados.")
    
async def escribirAtodos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "".join(context.args)
    for user_id in usuarios:
        try:
            await context.bot.send_message(chat_id=user_id, text=mensaje)
        except TelegramError as e:
            print(f"Error al enviar mensaje a {user_id}: {e}")