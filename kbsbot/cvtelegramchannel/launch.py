from kbsbot.cvtelegramchannel.services import *
from kbsbot.cvtelegramchannel.utils import *
from telegram import (ChatAction)
from telegram import (ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from telegram import ParseMode
import logging
from functools import wraps
from decouple import config

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHAT, HELP, LUGAR, ENVIAR, ESTADO, CONFIRMAR, EDAD = range(7)


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func


def start(update, context):
    """
    Whe starting starting the chatbot, this is the information presented.

    :param update: update object of chatbot

    :param context: context of conversation
    """
    user = update.message.from_user.first_name
    if user is None:
        user = update.message.from_user.username

    full_response = f"""
    !Hola! {user}, soy (NOMBREPENDIENTE) un asistente con la finalidad de entregarte informacion oportuna de la epidemia mundial del covid-19 en el Ecuador.\nPuedo resolver tus dudas de la siguiente manera (/opciones):
           """
    options, response = menu_keyboard()

    update.message.reply_text(full_response + response, reply_markup=options, one_time_keyboard=True,
                              parse_mode=ParseMode.MARKDOWN)


@send_typing_action
def chat(update, context):
    """
    Chat method for the chatbot.

    :param update: update object of chatbot

    :param context: context of conversation
    """
    logger.info("[CHAT] %s", update)

    entidades = update.message.parse_entities()
    error_flag = False
    if len(entidades) > 0:
        raw_input = update.message.text
        comando_parts = None
        for entity in entidades:
            comando_parts = entity
            break
        comando = raw_input[comando_parts["offset"] + 1:comando_parts["length"]]
        comando_obj = find_comando(comando)
        logger.info("[COMANDO]: %s", comando_obj)
        if comando_obj is not None:
            if "answer" in comando_obj:
                update.message.reply_text(comando_obj["answer"])
            else:
                chat_flag = False
                if comando_obj["parent"]:
                    options, response = child_menu(comando_obj)
                    if options is not None or response is not None:
                        update.message.reply_text(response, reply_markup=options, one_time_keyboard=True,
                                                  parse_mode=ParseMode.MARKDOWN)
                    else:
                        chat_flag = True
                else:
                    chat_flag = True

                if chat_flag:
                    user_name = update.message.from_user.username
                    name = update.message.from_user.first_name
                    last_name = update.message.from_user.last_name
                    id_account = update.message.chat_id
                    # Preparing data
                    data = {"user_name": user_name,
                            "name": name, "last_name": last_name,
                            "social_network_id": id_account,
                            "comando": comando}

                    logger.info("[CHAT] >>>>> SentData  %s", data)
                    resp = dummy_service(data)
                    logger.info("[CHAT] <<<<< ReceivedData %s", data)
                    for ans in resp["answer"]:
                        if ans["answer_type"] == "text":
                            update.message.reply_text(ans["answer"], reply_markup=ReplyKeyboardRemove())
        else:
            error_flag = False

    else:
        error_flag = True
    if error_flag:
        update.message.reply_text("Recuerda usar los comandos provistos.\nUsando el comando /opciones")


def cancel(bot, update):
    return ConversationHandler.END


@send_typing_action
def ayuda(update, context):
    """
    Help method for the chatbot.

    :param update: update object of chatbot

    :param context: context of conversation
    """
    logger.info("[HELP] %s", update)
    options, response = menu_keyboard()
    update.message.reply_text(
        "Soy un asistente con la finalidad de entregarte informacion oportuna de la epidemia mundial del covid-19 en el Ecuador.\n"
        "Puedo resolver tus dudas de la siguiente manera\n" + response,
        reply_markup=options, one_time_keyboard=True,
        parse_mode=ParseMode.MARKDOWN)


@send_typing_action
def reporte(update, context):
    logger.info("[REPORTE] %s", update)
    context.chat_data["reporte"] = {}
    update.message.reply_text(
        "Recuerda que soy un robot.\n"
        "Ingresa la informacion del reporte paso a paso y presiona el boton enviar.\n"
        "Ingresa el lugar del caso reportado? \n"
        "En caso de no contar con la informacion presiona el boton /omitir")
    return LUGAR


# @send_typing_action
# def paciente(update, context):
#     logger.info("[PACIENTE] %s", update)
#     context.chat_data["reporte"]["nombre"] = update.message.text
#     update.message.reply_text("Ingresa el lugar del caso reportado.\n"
#                               "Puedes usar la opcion de mapas o describir la locacion\n"
#                               "En caso de no contar con la informacion presiona el boton /omitir")
#     return LUGAR


@send_typing_action
def skip_paciente(update, context):
    context.chat_data["reporte"]["nombre"] = "Desconocido"
    update.message.reply_text("Ingresa el lugar del caso reportado.\n"
                              "Puedes usar la opcion de mapas o describir la locacion\n"
                              "En caso de no contar con la informacion presiona el boton /omitir")
    return LUGAR


@send_typing_action
def skip_lugar(update, context):
    context.chat_data["reporte"]["lugar"] = "Desconocido"
    update.message.reply_text("Cual es estado del paciente?.\n", reply_markup=estado_keyboard(), one_time_keyboard=True,
                              parse_mode=ParseMode.MARKDOWN)
    return ESTADO


@send_typing_action
def lugar_paciente(update, context):
    logger.info("[LUGAR] %s", update)

    text_location = update.message.text

    if text_location is not None:
        if text_location == "/omitir":
            context.chat_data["reporte"]["lugar"] = "Desconocido"
        else:
            context.chat_data["reporte"]["lugar"] = text_location
    else:
        context.chat_data["reporte"]["lugar"] = update.message.location

    update.message.reply_text("Cual es estado del paciente?.", reply_markup=estado_keyboard(), one_time_keyboard=True,
                              parse_mode=ParseMode.MARKDOWN)
    return ESTADO


@send_typing_action
def estado(update, context):
    logger.info("[ESTADO] %s", update)
    if update.message.text == "/omitir":
        context.chat_data["reporte"]["estado"] = "Desconocido"
    else:
        context.chat_data["reporte"]["estado"] = update.message.text

    update.message.reply_text("Cual es la edad del paciente?", parse_mode=ParseMode.MARKDOWN)
    return EDAD


@send_typing_action
def edad(update, context):
    logger.info("[EDAD] %s", update)
    context.chat_data["reporte"]["edad"] = update.message.text

    lugar = context.chat_data['reporte']['lugar']
    local_estado = context.chat_data['reporte']['estado']
    local_edad = context.chat_data['reporte']['edad']
    if isinstance(local_estado, dict):
        local_estado = "Mapa"

    response = f"Esta es la informacion brindad:\n" \
               f"LUGAR = {lugar}\n" \
               f"ESTADO = {local_estado}\n" \
               f"EDAD = {local_edad}\n" \
               f"Deseas confirmar?.\nSelecciona no si quieres corregir los datos"
    update.message.reply_text(response, reply_markup=si_no_keyboard(), one_time_keyboard=True,
                              parse_mode=ParseMode.MARKDOWN)

    return CONFIRMAR


@send_typing_action
def confirmar_reporte(update, context):
    logger.info("[CONFIRMAR] %s", update)
    if update.message.text.lower() == "si":
        return ENVIAR
    else:
        update.message.reply_text("Vuelve a intentarlo para corregir la informacion",
                                  reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


@send_typing_action
def enviar_reporte(update, context):
    data = context.chat_data["reporte"]
    logger.info("[REPORTE] >>>>> SentData  %s", data)
    dummy_service(context.chat_data["reporte"])
    update.message.reply_text("Gracias por la informacion.\n"
                              "Se ha enviado tu reporte",
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text("Ha ocurrido un error inesperado. Vuelva a Intentarlo")


API_KEY = config("API_KEY")

if config("DEBUG", default=True, cast=bool):
    def run(updater):
        logger.info("MODE: DEVELOP")
        updater.start_polling()
        updater.idle()
else:
    def run(updater):
        logger.info("MODE: PRODUCTION")
        # add handlers
        updater.start_webhook(listen="0.0.0.0",
                              port=config("PORT", default="8443"),
                              url_path=API_KEY)
        updater.bot.set_webhook(config("WEBHOOK_URL") + API_KEY)

    # updater.start_webhook(config("LISTEN"),
    #                       config("PORT"),
    #                       config("URL_PATH"),
    #                       config("KEY"),
    #                       config("CERT"),
    #                       config("WEBHOOK_URL"))

if __name__ == '__main__':
    # Launching App
    logger.info("Starting bot")
    updater = Updater(API_KEY, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # updater.dispatcher.add_handler(CallbackQueryHandler(button))

    conv_handler = ConversationHandler(
        entry_points=[
            # MessageHandler(Filters.regex(r'^(start|iniciar|comenzar|Start|Iniciar|Comenzar)$'), start),
            # MessageHandler(Filters.regex(r'^(ayuda|Ayuda|menu|Menu)$'), ayuda),
            CommandHandler('ReportarCaso', reporte),
            CommandHandler('start', start),
            CommandHandler('iniciar', start),
            # CommandHandler('comenzar', start),
            # CommandHandler('ayuda', ayuda),
            CommandHandler('opciones', ayuda),
            CommandHandler('menu', ayuda),
            MessageHandler(Filters.regex('.'), chat),
            # RegexHandler('\w', chat),
            # CommandHandler('cursos', chat),
        ],

        states={
            CHAT: [MessageHandler(Filters.text, chat)],
            # PACIENTE: [MessageHandler(Filters.text, paciente)],
            LUGAR: [MessageHandler(Filters.location, lugar_paciente),
                    MessageHandler(Filters.text, lugar_paciente),
                    CommandHandler('omitir', skip_paciente)],
            ESTADO: [MessageHandler(Filters.text, estado),
                     CommandHandler('omitir', skip_lugar)],
            EDAD: [MessageHandler(Filters.text, edad)],
            CONFIRMAR: [MessageHandler(Filters.text, confirmar_reporte)],
            ENVIAR: [MessageHandler(Filters.text, enviar_reporte)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)
    run(updater)
    # main()
