from django.http import JsonResponse

from .utils import Dictionarizable, BotException, normalize_string

from .chat_api.chat import Chatbot


class Message(Dictionarizable):
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content

    def dict(self) -> dict:
        """
        @return
        dictionary with the contents of the message
        """
        return {
            'message': {
                'sender': self.sender,
                'content': self.content
            }
        }

    def json_response(self, status):
        """
        Converts the message into a JsonResponse object
        """
        return JsonResponse(self.dict(), status=status)


class BotMessage(Message):
    def __init__(self, content):
        super().__init__("bot", content)


class UserMessage(Message):
    def __init__(self, content):
        super().__init__("user", content)


class MessageHistory:

    def __init__(self):
        self.message_history = []

    def __str__(self):
        return [msg for msg in self.messages()].__str__()

    def add(self, message: Message):
        self.message_history.append(message)

    def messages(self):
        for message in self.message_history:
            yield {"sender": message.sender, "content": message.content}


class MessageProcessor:

    def __init__(self, cache: dict):
        self.cache = cache
        self.chatbot = cache['chatbot'] if cache.get('chatbot') else Chatbot()

    def process_message(self, message) -> Dictionarizable:
        answer = self.chatbot.send_message(message)

        return BotMessage(answer)


class ErrorResponse(JsonResponse):
    def __init__(self, content=None, **kwargs):
        kwargs.setdefault('status', 500)
        if content is None:
            content = "Beep-bop! Something went wrong... Please try again later..."

        super().__init__(BotMessage(content).dict(), **kwargs)
