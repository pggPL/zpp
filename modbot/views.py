import logging

from django.http import HttpResponse
from django.shortcuts import render

from modbot.bot_client import BotClient


# Create your views here.
def run_bot(request):
    logging.info("Starting bot...")
    BotClient.run_bot()
    return HttpResponse("bot started")
