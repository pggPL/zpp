import discord
from discord.ui import View

from app_main.models import Submission, SubmissionCategory
from modbot.async_db_client import *


class DoneSubmissionView:
    def __init__(self, submission: Submission, controller, view_id: int):
        self.submission = submission
        self.controller = controller
        self.view_id = view_id
        self.message = None

    async def make_message_embed(self):
        submission_category = await get_submission_category(self.submission)
        embed = discord.Embed(title=f"Submission", description=self.submission.link,
                              color=discord.Color.blue())
        embed.add_field(name="Category", value=submission_category.name, inline=False)
        return embed

    # for now no interactions
    async def display(self, channel):
        # submission_category = await get_submission_category(self.submission)
        # embed = discord.Embed(title=f"Submission", description=self.submission.link,
        #                       color=discord.Color.blue())
        # embed.add_field(name="Category", value=submission_category.name, inline=False)
        embed = await self.make_message_embed()
        self.message = await channel.send(embed=embed)
        await channel.send("\u200B")

    async def update(self, submission: Submission):
        self.submission = submission
        embed = await self.make_message_embed()
        await self.message.edit(embed=embed)
