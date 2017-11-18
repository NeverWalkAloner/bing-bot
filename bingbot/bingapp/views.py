import io
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.http.response import JsonResponse
from .generic import get_urls, get_full_url, get_file, get_dates
from django.conf import settings
import json
import telebot
from telebot import types


# Create your views here.
class BiPiView(View):
    bot = telebot.TeleBot(settings.TGRM_TOKEN)

    def post(self, request, *args, **kwargs):
        test = request.body.decode('utf-8')
        body = json.loads(test)
        try:
            date = body['inline_query']['query']
            picture = get_urls(date)
            if picture:
                t = picture['copyright']
                full_url = get_full_url(picture)
                query_result = types.InlineQueryResultArticle(
                    id="1",
                    title=t,
                    input_message_content=types.InputTextMessageContent(full_url)
                )
            else:
                t = 'Image not found'
                r = 'Image not found'
                query_result = types.InlineQueryResultArticle(
                    id="1",
                    title=t,
                    input_message_content=types.InputTextMessageContent(r)
                )
            self.bot.answer_inline_query(
                body['inline_query']['id'],
                [query_result, ]
            )
            return JsonResponse({})
        except KeyError:
            date = body['message']['text']
        chat_id = body['message']['chat']['id']
        text_help = "Just start with /image command."
        if date == '/help':
            self.bot.send_message(chat_id, text_help)
        elif date == '/start':
            self.bot.send_message(chat_id, text_help)
        elif date == '/image':
            try:
                markup = types.ReplyKeyboardMarkup()
                dates = get_dates()
                buttons = [types.KeyboardButton(d) for d in dates]
                markup.add(*buttons)
                self.bot.send_message(chat_id,
                                      'Choose the date:',
                                      reply_markup=markup)
            except:
                self.bot.send_message(chat_id,
                                      'I am in a bad mood:( Try later.')
        else:
            try:
                picture = get_urls(date)
                if picture:
                    description = picture['copyright']
                    full_url = get_full_url(picture)
                    markup = types.ReplyKeyboardRemove()
                    self.bot.send_message(chat_id,
                                          'working on it...',
                                          reply_markup=markup)
                    file_bytes = io.BytesIO(get_file(full_url))
                    file_bytes.name = f'{date}.jpg'
                    self.bot.send_document(chat_id, file_bytes)
                    self.bot.send_message(chat_id, description)
                else:
                    self.bot.send_message(chat_id, "Image not found")
            except:
                self.bot.send_message(chat_id,
                                      'I am in a bad mood:( Try later.')
        return JsonResponse({})

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(BiPiView, self).dispatch(request, *args, **kwargs)
