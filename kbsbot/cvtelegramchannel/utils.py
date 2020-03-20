from telegram import InlineKeyboardButton, ReplyKeyboardMarkup

FULL_OPCIONES = [
    # {"comando": "Menu", "parent": True},
    {"comando": "Prevencion", "description": "Enterate de las medidas de prevencion en diferentes medios",
     "parent": True,
     "child": ["Transporte", "Hogar", "Trabajo"]},
    {"comando": "Transporte", "description": "Medidas de movilización", "parent": False},
    {"comando": "Hogar", "description": "Medidas de prevencion en el hogar", "parent": False},
    {"comando": "Trabajo", "description": "Medidas de prevencion para tu trabajo", "parent": False},
    {"comando": "CentrosHabilitados", "description": "Conoce los centros habilitados en el pais", "parent": True,
     "child": ["PorProvincia", "PorCiudad"]},
    {"comando": "PorProvincia", "description": "Centros médicos disponibles", "parent": False},
    {"comando": "PorCiudad", "description": "Centros médicos disponibles ", "parent": False},
    {"comando": "Sintomas", "description": "Sintomas relacionado al cuadro de una persona con covid-19",
     "parent": True},
    {"comando": "HerramientasTeletrabajo", "description": "Herramientas que te pueden interesar", "parent": True,
     "child": ["Educacion", "Teletrabajo"]},
    {"comando": "Educacion", "description": "Herramientas para profesores y estudiantes", "parent": False},
    {"comando": "Teletrabajo", "description": "Herramientas para el trabajo desde casa", "parent": False},
    {"comando": "EstadoCuarentena", "description": "Ultimas noticias de la cuarentena", "parent": True},
    {"comando": "MediosComunicacion", "description": "Medios oficiales para informarte", "parent": True},
    {"comando": "UltimasNoticias", "description": "Qué pasa con el covid-19 a nivel mundial", "parent": True},
    {"comando": "ReportarCaso", "description": "Cónoces algún caso? Reportalo", "parent": True},
    {"comando": "ComoColaborar", "answer": "Puedes colaborar escribiendonos al 0987368191",
     "description": "Contacta con nostros!", "parent": True},
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
