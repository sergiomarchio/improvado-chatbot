import functools
import traceback

from django.core.exceptions import BadRequest
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ChatForm
from .models import MessageHistory, MessageProcessor, \
    Message, BotMessage, UserMessage, \
    ErrorResponse


def clear(request):
    """
    Clears the chat and the session
    """

    print('Clearing chat and session info...')

    request.session.flush()
    request.session['cache'] = {}

    return HttpResponseRedirect(reverse('chatbot:chat'))


def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def require_ajax(view):
    """
    Decorator to allow only AJAX requests in the decorated view
    """
    @functools.wraps(view)
    def wrapper(request):
        if not is_ajax(request):
            print("request is not AJAX...")
            raise BadRequest

        return view(request)

    return wrapper


@require_ajax
@require_POST
def process_message(request):
    """
    Processes the message from the user (sent via AJAX) and returns the bot response.
    """
    if 'cache' not in request.session:
        print('cache not in request.session')
        return ErrorResponse()
    elif 'message_history' not in request.session:
        print('message_history not in request.session')
        return ErrorResponse()

    chat_form = ChatForm(request.POST)

    if not chat_form.is_valid():
        print("Invalid form... ChatForm")
        return ErrorResponse()

    user_message_content = chat_form.cleaned_data['text_field']
    user_message = UserMessage(user_message_content)

    request.session['message_history'].add(user_message)

    try:
        processing_result = MessageProcessor(request.session['cache']).process_message(user_message_content)
    except Exception as e:
        print("Exception: ", e)
        print(traceback.format_exc())
        print(f"While processing message {user_message_content}")

        return ErrorResponse()

    if isinstance(processing_result, Message):
        request.session['message_history'].add(processing_result)

    print()
    print(processing_result)

    return JsonResponse(processing_result.dict(), status=200)


def chat(request):
    """
    Main view for chat window.
    The first time it's loaded, it creates a welcome message
    """

    if 'message_history' not in request.session:
        clear(request)
        messages = MessageHistory()
        messages.add(BotMessage('Hi! how can I help you today?'))
        request.session['message_history'] = messages

    form = ChatForm()

    context = {
        'form': form,
        'message_history': request.session['message_history']
    }

    return render(request, 'chatbot/chat.html', context)
