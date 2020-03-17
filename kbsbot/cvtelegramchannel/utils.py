from telegram import InlineKeyboardButton

FULL_OPCIONES = [
    # {"comando": "Menu", "parent": True},
    {"comando": "Prevencion", "description": "Lorem", "parent": True,
     "child": ["PrevencionTransporte", "PrevencionHogar", "PrevencionTrabajo"]},
    {"comando": "PrevencionTransporte", "description": "Lorem", "parent": False},
    {"comando": "PrevencionHogar", "description": "Lorem", "parent": False},
    {"comando": "PrevencionTrabajo", "description": "Lorem", "parent": False},
    {"comando": "CentrosHabilitados", "description": "Lorem", "parent": True, "child": ["CHProvincia", "CHCiudad"]},
    {"comando": "CHProvincia", "description": "Lorem", "parent": False},
    {"comando": "CHCiudad", "description": "Lorem", "parent": False},
    {"comando": "Sintomas", "description": "Lorem", "parent": True},
    {"comando": "HerramientasTeletrabajo", "description": "Lorem", "parent": True,
     "child": ["HTEducacion", "HTTeletrabajo"]},
    {"comando": "HTEducacion", "description": "Lorem", "parent": False},
    {"comando": "HTTeletrabajo", "description": "Lorem", "parent": False},
    {"comando": "EstadoCuarentena", "description": "Lorem", "parent": False},
    {"comando": "MediosComunicacion", "description": "Lorem", "parent": False},
    {"comando": "ComoColaborar", "description": "Lorem", "parent": False},
    {"comando": "ReportarCaso", "description": "Lorem", "parent": True},
    {"comando": "UltimasNoticias", "description": "Lorem", "parent": False},
    {"comando": "ComoColaborar", "answer": "Puedes colaborar escribiendonos a", "description": "Lorem", "parent": True},
]


def estado_keyboard():
    estado_paciente = [{"comando": "Confirmado"}, {"comando": "No confirmado"}, {"comando": "Desconocido"}]
    return prepare_keyboard(estado_paciente, command=False)


def prepare_keyboard(options, command=True):
    keyboard = []
    for option in options:
        if command:
            keyboard.append([InlineKeyboardButton("/" + option["comando"])])
        else:
            keyboard.append([InlineKeyboardButton(option["comando"])])
    return keyboard


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
    resp = None
    for opcion in FULL_OPCIONES:
        if opcion["comando"] == comando:
            resp = opcion
    return resp


def child_menu(comando):
    local_options = []
    if "child" in comando:
        for child_comand in comando["child"]:
            local_options.append(find_comando(child_comand))
        return prepare_keyboard(local_options), options_description(local_options)
    else:
        return None, None
