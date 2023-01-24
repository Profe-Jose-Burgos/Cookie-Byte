from chatbot_processing import predict_class, get_response
from gsheet_func import *
from scrapAmazon import RunAmazon
import json

from datetime import datetime
from datetime import date
from dateutil.parser import parse

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

intents_mode = 'intents3.json'
dt=date.today().strftime('%d/%m/%Y')
now_date = datetime.strptime(dt,'%d/%m/%Y')

special_tags=["soliciar_cita",'cotizacion','envio']
scrapper = RunAmazon()

intents = json.loads(
    open(intents_mode).read().encode("latin_1").decode("utf_8"))

app = Flask(__name__)


@app.route('/chatbot', methods=['POST'])
def chatbot():
    incoming_msg = request.form.get('Body').lower()
    #incoming_msg = unidecode.unidecode(incoming_msg)
    response = MessagingResponse()
    message = response.message()
    responded = False
    word_sub = incoming_msg.split('@')

    ints = predict_class(incoming_msg)
    res, tag = get_response(ints, intents)

    if "solicitar_cita" == tag:
        # reply = "¿Desea agendar una cita?"
        # "Por supuesto!, para solicitar una cita necesito lo siguiente: \n "
        # message.body(reply)
        responded = True

        if len(word_sub) == 1 and "si" in incoming_msg:
            cita_string = "Por supuesto!, para solicitar una cita necesito lo siguiente: \n \n Ingresa la fecha de la cita en este formato\n"\
                "*Fecha @* _fecha aqui_ "
            message.body("")
            message.body(cita_string)
            responded = True
        elif len(word_sub) == 1 and "no" in incoming_msg:
            reply = "Ok. Que tenga un buen dia!"
            message.body(reply)
            responded = True
        else:
            message.body(res)

    elif "cotizacion" == tag:
        responded = True

        if len(word_sub) == 1 and "si" in incoming_msg:
            cita_string = "Por supuesto!, para cotizar necesito lo siguiente: \n \n Ingresa el enlace del producto a cotizar en el siguiente formato.\n"\
                "*Link @* _enlace aqui_ "
            message.body(cita_string)
            responded = True
        elif len(word_sub) == 1 and "no" in incoming_msg:
            reply = "Ok. Que tenga un buen dia!"
            message.body(reply)
            responded = True
        else:
            message.body(res)

    elif "envio" == tag:
        print('algo')

    elif len(word_sub) != 1:
        tipo_input = word_sub[0].strip()
        string_input = word_sub[1].strip()
        if tipo_input == 'fecha':
            reply = "Ingrese informacion relevante a su cita por agendar. Utilice el siguiente formato. \n\n"\
                "*Info @* _escriba la informacion_"
            if set_fecha_cita(string_input) == 0:
                message.body(reply)
                responded = True
            else:
                responded = False

        if tipo_input == 'info':
            reply = "Su cita ha sido agendada!"
            set_info_cita(string_input)
            message.body(reply)
            responded = True

        if tipo_input == 'link':
            #Anadir aqui la llamada al codigo de diana.
            #reply = "Su cita ha sido agendada!"
            if "https://www.amazon.com/" in string_input:
                reply = scrapper.scrape(string_input) #scrapping
                message.body(reply)
                responded = True
            else:
                responded = False

    elif tag not in special_tags:
        message.body(res)
        responded = True

    if not responded:
        message.body(
            'Formato incorrecto. Porfavor utilice el formato correcto.')

    # message.body(res)
    return str(response)

def set_fecha_cita(msg):
    p = parse(msg)
    date=p.strftime('%d/%m/%Y')
    if p > now_date:
        guardar_fecha_cita(date)
        return 0
    return 1

def set_info_cita(msg):
    guardar_info_cita(msg)
    return 0