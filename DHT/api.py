from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
import requests
# Définir la fonction pour envoyer des messages Telegram
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response
@api_view(["GET", "POST"])
def Dlist(request):
    if request.method == "GET":
        all_data = Dht11.objects.all()
        data_ser = DHT11serialize(all_data, many=True)  # Les données sont sérialisées en JSON
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(derniere_temperature)

            if serial.is_valid():
                serial.save()
                derniere_temperature = Dht11.objects.last().temp
                print(derniere_temperature)

                if derniere_temperature > 20:
                    # Alert Email
                    #subject = 'Alerte'
                    #message = 'La température dépasse le seuil de 20°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    #email_from = settings.EMAIL_HOST_USER
                    #recipient_list = ['ouissal.belarbi2020@gmail.com']
                    #send_mail(subject, message, email_from, recipient_list)

                    # Alert WhatsApp
                    account_sid = 'ACfe9cac30a59aeb7292f600d04ea2b68e'
                    auth_token = 'af4158c07b9a95fcdf7c9ecc306d0ff0'
                    client = Client(account_sid, auth_token)
                    message_whatsapp = client.messages.create(
                        from_='whatsapp:+14155238886',
                        body='La température dépasse le seuil de 20°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation',
                        to='whatsapp:+212702662395'
                    )

                    # Alert Telegram
                    telegram_token = '7527849044:AAHophVAunnJX8_SLu9_4ImuKTG8ntaP_-g'
                    chat_id = '5264942598'  # Remplacez par votre ID de chat
                    telegram_message = 'La température dépasse le seuil de 20°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    send_telegram_message(telegram_token, chat_id, telegram_message)

                return Response(serial.data, status=status.HTTP_201_CREATED)

            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)