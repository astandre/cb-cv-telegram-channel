from telegram import InlineKeyboardButton, ReplyKeyboardMarkup

FULL_OPCIONES = [
    # {"comando": "Menu", "parent": True},
    {"comando": "Prevencion", "description": "Lorem", "parent": True,
     "child": ["Transporte", "Hogar", "Trabajo"]},
    {"comando": "Transporte", "description": "Lorem", "parent": False},
    {"comando": "Hogar", "description": "Lorem", "parent": False},
    {"comando": "Trabajo", "description": "Lorem", "parent": False},
    {"comando": "CentrosHabilitados", "description": "Lorem", "parent": True, "child": ["PorProvincia", "PorCiudad"]},
    {"comando": "PorProvincia", "description": "Lorem", "parent": False},
    {"comando": "PorCiudad", "description": "Lorem", "parent": False},
    {"comando": "Sintomas", "description": "Lorem", "parent": True},
    {"comando": "HerramientasTeletrabajo", "description": "Lorem", "parent": True,
     "child": ["Educacion", "Teletrabajo"]},
    {"comando": "Educacion", "description": "Lorem", "parent": False},
    {"comando": "Teletrabajo", "description": "Lorem", "parent": False},
    {"comando": "EstadoCuarentena", "description": "Lorem", "parent": False},
    {"comando": "MediosComunicacion", "description": "Lorem", "parent": False},
    {"comando": "UltimasNoticias", "description": "Lorem", "parent": False},
    {"comando": "ReportarCaso", "description": "Lorem", "parent": True},
    {"comando": "ComoColaborar", "answer": "Puedes colaborar escribiendonos a", "description": "Lorem", "parent": True},
]


def estado_keyboard():
    estado_paciente = [{"comando": "En cuarentena domiciliar"}, {"comando": "Internado"}, {"comando": "Desconocido"}]
    return prepare_keyboard(estado_paciente, command=False)


def si_no_keyboard():
    estado_paciente = [{"comando": "Si"}, {"comando": "No"}]
    return prepare_keyboard(estado_paciente, command=False)


def prepare_keyboard(options, command=True):
    keyboard = []
    for option in options:
        if command:
            keyboard.append([InlineKeyboardButton("/" + option["comando"])])
        else:
            keyboard.append([InlineKeyboardButton(option["comando"])])
    return ReplyKeyboardMarkup(keyboard)


def menu_keyboard():
    parent_options = []
    for option in FULL_OPCIONES:
        if option["parent"]:
            parent_options.append(option)
    return prepare_keyboard(parent_options), options_description(parent_options)


def options_description(local_options):
    response = ""
    for option in local_options:
        if "description" in option:
            response += f"- /{option['comando']} {option['description']} \n"
        else:
            response += f"- /{option['comando']}\n"
    return response


def find_comando(comando):
    for opcion in FULL_OPCIONES:
        if opcion["comando"] == comando:
            return opcion


def child_menu(comando):
    local_options = []
    if "child" in comando:
        for child_comand in comando["child"]:
            local_options.append(find_comando(child_comand))
        return prepare_keyboard(local_options), options_description(local_options)
    else:
        return None, None
