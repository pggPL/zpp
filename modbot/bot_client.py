import asyncio
import threading

import discord

from modbot.bot import ModBot
from app_main.models import Submission


class BotClient:
    bot_thread = None
    bot_object: ModBot = None
    token = ""
    token_file_name = "modbot/token.txt"

    @classmethod
    def add_submission(cls, submission: Submission):
        task = asyncio.run_coroutine_threadsafe(cls.bot_object.add_new_submission(submission), cls.bot_object.loop)
        return task.result()

    @classmethod
    def load_token(cls):
        with open(cls.token_file_name, 'r') as f:
            cls.token = f.read().strip()

    # start bot in a new thread
    @classmethod
    def run_bot(cls):
        if not cls.token:
            cls.load_token()

        # Each time when running bot create new bot object
        intents = discord.Intents.all()
        intents.message_content = True
        intents.messages = True
        cls.bot_object = ModBot(command_prefix='/', intents=intents)

        # start the bot
        def bot_runner():
            cls.bot_object.run(cls.token)

        cls.bot_thread = threading.Thread(target=bot_runner)
        cls.bot_thread.start()


