import requests



def telegram_api(texto,numero_chat):
    requests.post('https://api.telegram.org/bot2114681560:AAGPlALNSj-TWi2ipYkkyJ7r6oKbKkJGdz0/sendMessage',
                  data={'chat_id': numero_chat, 'text': texto})
