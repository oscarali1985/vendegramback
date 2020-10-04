
import os
import requests
from flask import  jsonify

def telegram_bot_sendtext(bot_message):
    
    bot_token = os.environ.get('TOKEN_TELE')
    bot_chatID = '677779190'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message



    response = requests.get(send_text)
    print(response)
    return response.json()


def sendTelegram(nombre,telegram,mensaje):

    bot_message = "Buen dia "+ nombre +"\n"+" "+"\n"+mensaje

    bot_token = os.environ.get('TOKEN_TELE')
    bot_chatID = telegram
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    print(response)
    y = response.json()
    ok = y['ok']
    #Cuando se envia se muestran estos resultados
    if ok  == True:
        resul = y['result']
        print(resul)
        print(ok)
        Mensaje = "El mensaje fue enviado"
        #flash(Mensaje, 'alert-success')
        return jsonify(Mensaje), 200
    else :
        descrip = y['description']
        errorCode = y['error_code']
        ok = y['ok']
        cuentabot= "@OamdBot"
        mensaje2 = "La pesona debe seguirnos y activar el boot "+ cuentabot + "en telegram para que pueda recibir nuestros mensajes"
        Mensaje = "El mensaje no pudo ser enviado error {} "+descrip+ "\n"+ mensaje2

        #flash(Mensaje.format(errorCode), 'alert-danger')
        return jsonify(Mensaje), 400
    