# Telegram Channel
[![Build Status](https://travis-ci.org/astandre/cb-cv-telegram-channel.svg?branch=master)](https://travis-ci.org/astandre/cb-cv-telegram-channel)

Chatbot desarrollado para presentar informacion util acerca de la pandemia del Covid-19 en Ecuador.


## Configuracion

1. Instalar los requerimientos

```shell script
pip install -r requirements.txt
```

2. Crear un archivo .env dentro de la carpeta *kbsbot/cvtelegramchannel* con la siguiente informacion.

```
DEBUG=True
API_KEY=TELEGRAM_KEY
BASE_URL=http://127.0.0.1:5005
```
 

## Guia de despliegue

En caso de despliegue configurar los siguientes parametros adicionales y seguir con [Guia](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks)

```
DEBUG=False
LISTEN=0.0.0.0
PORT=8443
URL_PATH=TOKEN
KEY=private.key
CERT=cert.pem
WEBHOOK_URL=https://example.com:8443/TOKEN
```

## Despliegue con docker

Generar imagen 
```
docker build -t covid-bot-ec .
```

Ejecutar imagen

```
docker run --rm  --name=covid-bot-ec -p 8443:8443 -it covid-bot-ec
```

## Despliegue de heroku 

Visualizar logs

```
heroku logs --tail --app covid-bot-ec
```

