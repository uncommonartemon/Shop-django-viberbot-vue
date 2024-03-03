from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest, ViberMessageRequest
from django.http import HttpResponse

def handle_incoming_message(request):
    viber = Api(BotConfiguration(
        name='Torry',
        avatar='https://dl-media.viber.com/1/share/2/long/vibes/icon/image/0x0/a6e2/a766d536026af919e09a954479c009d0b554d60412d8798dd9298889425fa6e2.jpg',
        auth_token='5114b04a6a67e26d-47b8019b92f46735-b130ed77ec40cc8f'
    ))
    viber_request = viber.parse_request(request.body)
    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message.text
        sender_id = viber_request.sender.id
        
        # Обработка сообщения
        # Здесь вы можете добавить свою логику обработки сообщений от пользователя
        
        # Пример: Отправка ответного сообщения
        viber.send_messages(sender_id, [
            TextMessage(text='Спасибо за ваше сообщение!')
        ])

    return HttpResponse(status=200)
