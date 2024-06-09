import logging

import discord
from discord.ui import View, Select, Button

from app_main.models import Submission, SubmissionCategory


from modbot.async_db_client import *


class PendingSubmissionView:

    def __init__(self, submission: Submission, submission_category: SubmissionCategory,
                 controller, view_id: int):
        self.submission = submission
        self.controller = controller
        self.view_id = view_id
        self.categories = controller.categories

        # save the view message here when the view is rendered
        self.message = None

        # pass the current submission category to avoid async db operation in init
        self.submission_category = submission_category

        # for now use single discord View to handle button and category select
        self.view = View(timeout=None)

        # dynamically prepare discord view interactive items
        self.prepare_category_select()
        self.prepare_done_button()

    def prepare_done_button(self):
        button = Button(label="mark as done", style=discord.ButtonStyle.green, row=2)

        async def callback(interaction):
            await self.controller.on_done_clicked(interaction, self)

        button.callback = callback
        self.view.add_item(button)

    def prepare_category_select(self):
        options = []
        for category in self.categories:
            new_option = discord.SelectOption(label=category.name, value=category.id)
            # when making the menu mark the current category as default,
            # so it can be initially displayed
            if category.id == self.submission_category.id:
                new_option.default = True
            options.append(new_option)

        select = Select(options=options, row=1)

        async def callback(interaction):
            await self.controller.on_category_select(interaction, select, self)

        select.callback = callback

        self.view.add_item(select)

    async def display(self, channel):
        # save the message
        self.message = \
            await channel.send(content=f"\u200B\nlink: {self.submission.link}", view=self.view)

    async def update(self, submission):
        self.submission = submission
        self.submission_category = await get_submission_category(submission)

        # prepare new view after updating submission and category
        self.view = View(timeout=None)
        self.prepare_category_select()
        self.prepare_done_button()

        # update the message
        await self.message.edit(view=self.view)

