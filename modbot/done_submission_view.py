import discord
from discord.ui import View

from app_main.models import Submission, SubmissionCategory
from modbot.async_db_client import *


class DoneSubmissionView:
    def __init__(self, submission: Submission, controller, view_id: int):
        self.submission = submission
        self.controller = controller
        self.view_id = view_id

    # for now no interactions
    async def display(self, channel):
        submission_category = await get_submission_category(self.submission)
        embed = discord.Embed(title=f"Submission", description=self.submission.link,
                              color=discord.Color.blue())
        embed.add_field(name="Category", value=submission_category.name, inline=False)
        await channel.send(embed=embed)
