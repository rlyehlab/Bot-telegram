from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes
from database.db import guardar_usuario, obtener_todos_usuarios
from datetime import time, timezone

async def recordatorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.effective_message
    chat = update.effective_chat

    if mensaje is None or chat is None:
        return

    args = context.args or []
    if len(args) != 1:
        await mensaje.reply_text("Uso: /recordatorio <dia del mes>, por ejemplo /recordatorio 15")
        return

    try:
        dia_solicitado = int(args[0])
    except ValueError:
        await mensaje.reply_text("El dia debe ser un numero entre 1 y 31.")
        return

    if not 1 <= dia_solicitado <= 31:
        await mensaje.reply_text("El dia debe estar entre 1 y 31.")
        return

    job_queue = context.job_queue
    if job_queue is None:
        await mensaje.reply_text("La cola de tareas no está disponible.")
        return

    dia_programado = dia_solicitado if dia_solicitado <= 27 else -1
    nombre_job = f"recordatorio_mensual_{chat.id}"

    for job in job_queue.get_jobs_by_name(nombre_job):
        job.schedule_removal()

    job_queue.run_monthly(
        enviar_recordatorio,
        when=time(hour=9, minute=0, tzinfo=timezone.utc),
        day=dia_programado,
        data={"chat_id": chat.id, "texto": "Este es tu recordatorio mensual."},
        name=nombre_job,
    )

    if dia_programado == -1:
        confirmacion = "el ultimo dia de cada mes"
    else:
        confirmacion = f"el dia {dia_programado} de cada mes"
    await mensaje.reply_text(
        f"Recordatorio programado para {confirmacion}, a las 09:00 UTC."
    )

async def enviar_recordatorio(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    if job is None or not isinstance(job.data, dict):
        return

    chat_id = job.data.get("chat_id")
    texto = job.data.get("texto")
    if not isinstance(chat_id, int) or not isinstance(texto, str):
        return

    await context.bot.send_message(chat_id=chat_id, text=texto)

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

async def guardaruser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    usuario = update.effective_user
    if usuario is None or update.message is None:
        return
    guardar_usuario(usuario.id, usuario.first_name, usuario.username)
    await update.message.reply_text(
        "usuario guardado")
    

async def mostrarusuarios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios = obtener_todos_usuarios()
    if usuarios:
        for usuario in usuarios:
            await update.message.reply_text(
                f"Usuarios guardados:\n telegram ID:{usuario['telegram_id']} \n username: {usuario['username']} \n \n"
            )
    else:
        await update.message.reply_text("No hay usuarios guardados.")
    
async def escribirAtodos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios = obtener_todos_usuarios()
    # mensaje = "".join(context.args)
    for usuario in usuarios:
        try:
            await context.bot.send_message(chat_id=usuario['telegram_id'], text='hola')
        except TelegramError as e:
            print(f"Error al enviar mensaje a {user_id}: {e}")