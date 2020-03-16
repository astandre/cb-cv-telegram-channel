from kbsbot.cvtelegramchannel.services import *
from kbsbot.cvtelegramchannel.utils import *
from telegram import (ChatAction)
from telegram import (ReplyKeyboardRemove, ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from telegram import ParseMode
import logging
from functools import wraps



# API_KEY = os.environ.get("API_KEY")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHAT, HELP, PACIENTE, LUGAR, ENVIAR, ESTADO = range(6)


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
        full_response = f"Hola {user}. En que te puedo ayudar?\n"
    else:
        full_response = f"Hola {user}. En que te puedo ayudar?\n"

    options, response = menu_keyboard()
    reply_markup = ReplyKeyboardMarkup(options)

    update.message.reply_text(full_response + response, reply_markup=reply_markup, one_time_keyboard=True,
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
                if comando_obj["parent"]:
                    options, response = child_menu(comando_obj)
                    reply_markup = ReplyKeyboardMarkup(options)
                    update.message.reply_text(response, reply_markup=reply_markup, one_time_keyboard=True,
                                              parse_mode=ParseMode.MARKDOWN)
                else:
                    user_name = update.message.from_user.username
                    name = update.message.from_user.first_name
                    last_name = update.message.from_user.last_name
                    id_account = update.message.chat_id

                    data_user = {"user_name": user_name,
                                 "name": name, "last_name": last_name,
                                 "social_network_id": id_account}
                    # Preparing data
                    data = {
                        "user": data_user,
                        "comando": comando
                    }
                    logger.info("[CHAT] >>>>> SentData  %s", data)
                    resp = dummy_service(data)
                    logger.info("[CHAT] <<<<< ReceivedData %s", data)
                    for ans in resp["answer"]:
                        if ans["answer_type"] == "text":
                            update.message.reply_text(ans["answer"])
        else:
            update.message.reply_text("Recuerda usar los comandos provistos")

    else:
        update.message.reply_text("Recuerda usar los comandos provistos")


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
    reply_markup = ReplyKeyboardMarkup(options)
    update.message.reply_text("hola ayuda\n" + response, reply_markup=reply_markup, one_time_keyboard=True,
                              parse_mode=ParseMode.MARKDOWN)


@send_typing_action
def reporte(update, context):
    logger.info("[REPORTE] %s", update)
    context.chat_data["reporte"] = {}
    update.message.reply_text(
        "Recuerda que soy un robot.\n"
        "Ingresa la informacion del reporte paso a paso.\n"
        "Cual es el nombre del paciente? \n"
        "En caso de no contar con la informacion presiona el boton /omitir")
    return PACIENTE


@send_typing_action
def paciente(update, context):
    logger.info("[PACIENTE] %s", update)
    context.chat_data["reporte"]["nombre"] = update.message.text
    update.message.reply_text("Ingresa el lugar del caso reportado.\n"
                              "Puedes usar la opcion de mapas o describir la locacion\n"
                              "En caso de no contar con la informacion presiona el boton /omitir")
    return LUGAR


@send_typing_action
def skip_paciente(update, context):
    context.chat_data["reporte"]["nombre"] = "Desconocido"
    update.message.reply_text("Ingresa el lugar del caso reportado.\n"
                              "Puedes usar la opcion de mapas o describir la locacion\n"
                              "En caso de no contar con la informacion presiona el boton /omitir")
    return LUGAR


@send_typing_action
def skip_lugar(update, context):
    reply_markup = ReplyKeyboardMarkup(estado_keyboard())
    context.chat_data["reporte"]["lugar"] = "Desconocido"
    update.message.reply_text("Cual es estado del paciente?.\n", reply_markup=reply_markup, one_time_keyboard=True,
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

    reply_markup = ReplyKeyboardMarkup(estado_keyboard())
    update.message.reply_text("Cual es estado del paciente?.\n", reply_markup=reply_markup, one_time_keyboard=True,
                              parse_mode=ParseMode.MARKDOWN)
    return ESTADO


@send_typing_action
def estado(update, context):
    logger.info("[ESTADO] %s", update)
    if update.message.text == "/omitir":
        context.chat_data["reporte"]["estado"] = "Desconocido"
    else:
        context.chat_data["reporte"]["estado"] = update.message.text
    return ENVIAR


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


def main():
    """
    Main method to create the chatbot object
    """
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # updater.dispatcher.add_handler(CallbackQueryHandler(button))

    conv_handler = ConversationHandler(
        entry_points=[
            # MessageHandler(Filters.regex(r'^(start|iniciar|comenzar|Start|Iniciar|Comenzar)$'), start),
            # MessageHandler(Filters.regex(r'^(ayuda|Ayuda|menu|Menu)$'), ayuda),
            CommandHandler('ReportarCaso', reporte),
            CommandHandler('iniciar', start),
            # CommandHandler('comenzar', start),
            # CommandHandler('ayuda', ayuda),
            CommandHandler('menu', ayuda),
            MessageHandler(Filters.regex('.'), chat),
            # RegexHandler('\w', chat),
            # CommandHandler('cursos', chat),
        ],

        states={
            CHAT: [MessageHandler(Filters.text, chat)],
            PACIENTE: [MessageHandler(Filters.text, paciente)],
            LUGAR: [MessageHandler(Filters.location, lugar_paciente),
                    MessageHandler(Filters.text, lugar_paciente),
                    CommandHandler('omitir', skip_paciente)],
            ESTADO: [MessageHandler(Filters.text, estado),
                     CommandHandler('omitir', skip_lugar)],
            ENVIAR: [MessageHandler(Filters.text, enviar_reporte)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    # Launching App
    logger.info("Starting bot")
    main()
