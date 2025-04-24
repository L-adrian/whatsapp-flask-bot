from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = 'my_verify_token'  # puede ser lo que tú quieras
ACCESS_TOKEN = 'EAAJrWZC6YJlYBO6ZBTFZBXZBnac6mpBS15Lb4e8ZCd97fTgzJbHk4Ojtxo5czZAlFwJveXHZA8lyGZCiLNiROu5ZAGuIZCUsGQ3HraTdiGcTyOi15MFAIBeFYzZB0z3Ghq6MYyK5cZA6cTvjOyaMpDTcQgSadPZA4CHBCO4v9kbhbiqHIb7TvAhr6k2x9GM4DCkUEoAchVnWWpjpDG0brbYKZAwpCeUQG6D7oZAOmw9yewZD'
PHONE_NUMBER_ID = '634123883116087'


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verificación de Meta
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Error de verificación'

    if request.method == 'POST':
        data = request.get_json()
        try:
            entry = data['entry'][0]['changes'][0]['value']
            message = entry['messages'][0]
            phone_number = message['from']
            text = message['text']['body']

            # Lógica de respuesta
            respuesta = f"Echo: {text}"
            enviar_mensaje(phone_number, respuesta)

        except Exception as e:
            print('Error:', e)

        return 'ok', 200


def enviar_mensaje(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    r = requests.post(url, json=payload, headers=headers)
    print('Respuesta Meta:', r.text)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto de Render o 5000 local
    app.run(host='0.0.0.0', port=port)