import discord
import asyncio

from discord.ext import commands

import logging

from app_main.models import Submission
from modbot.submission_controller import SubmissionsController

logging.basicConfig(level=logging.INFO)


# function to clear messages more slowly to avoid hitting discord
# api rate limits
async def clear_messages(channel):
    while True:
        # Attempt to delete messages in bulk (up to 100 at a time)
        deleted = await channel.purge(limit=100, before=None)
        if len(deleted) < 100:
            break
        await asyncio.sleep(1.5)


# If the channel of the given name does not exist, add it.
# Otherwise, purge the existing channel.
# Do it for all guilds.
async def set_fresh_channel(guild, channel_name):
    channel = discord.utils.get(guild.text_channels, name=channel_name)
    if channel is None:
        channel = await guild.create_text_channel(channel_name)
    else:
        await clear_messages(channel)
    return channel


class ModBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pending_channel_name = "pending"
        self.done_channel_name = "done"
        self.submissions_controller: SubmissionsController = None
        self.curr_guild = None
        self.running = False

    # search for a given channel in all guilds
    # wherever the channel is find send the message
    async def send_to_channel(self, channel_name, message):
        for guild in self.guilds:
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            if channel is not None:
                await channel.send(message)

    async def print_hi(self):
        for guild in self.guilds:
            channel = discord.utils.get(guild.text_channels, name=self.pending_channel_name)
            if channel is not None:
                await channel.send("Hi from modbot!")

    async def on_message(self, message):
        if message.author.bot:
            return

        await self.print_hi()

    async def add_new_submission(self, submission: Submission):
        await self.submissions_controller.add_submission(submission)

    async def on_ready(self):
        # indicate that the bot is running
        self.running = True

        # for now handle only one guild
        self.curr_guild = list(self.guilds)[0]

        guild = self.curr_guild

        pending_channel = await set_fresh_channel(guild, self.pending_channel_name)
        done_channel = await set_fresh_channel(guild, self.done_channel_name)
        self.submissions_controller = SubmissionsController(pending_channel, done_channel)

        # make the controller load data form db and render it
        await self.submissions_controller.init_from_db()



