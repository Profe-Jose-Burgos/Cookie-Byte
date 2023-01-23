from chatbot_processing import predict_class, get_response
import json

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

intents_mode = 'intents3.json'

intents = json.loads(
    open(intents_mode).read().encode("latin_1").decode("utf_8"))

app = Flask(__name__)


@app.route('/chatbot', methods=['POST'])
def chatbot():
    incoming_msg = request.form.get('Body').lower()
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

        elif len(word_sub) != 1:
            tipo_input = word_sub[0].strip()
            string_input = word_sub[1].strip()
            if tipo_input == 'fecha':
                reply = "Ingrese informacion relevante a su cita por agendar. Utilice el siguiente formato. \n\n"\
                    "*Info @* _escriba la informacion_"
                # set_fecha_cita(string_input)
                message.body(reply)
                responded = True

            if tipo_input == 'info':
                reply = "Su cita ha sido agendada!"
                # set_info_cita(string_input)
                message.body(reply)
                responded = True
        else:
            message.body(res)

    if "saludos" == tag:
        message.body(res)
        responded = True

    if not responded:
        message.body(
            'Formato incorrecto. Porfavor utilice el formato correcto.')

    # message.body(res)
    return str(response)
