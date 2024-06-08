import logging

import discord
from discord.ui import View, Select, Button

from app_main.models import Submission


class PendingSubmissionView:

    def __init__(self, submission: Submission, controller, view_id: int):
        self.submission = submission
        self.controller = controller
        self.view_id = view_id
        self.categories = controller.categories

        # for now use single discord View to handle button and category select
        self.view = View(timeout=None)

        # dynamically prepare discord view interactive items
        self.prepare_category_select()
        self.prepare_done_button()

    def prepare_done_button(self):
        button = Button(label="mark as done", style=discord.ButtonStyle.green)

        async def callback(interaction):
            await self.controller.on_done_clicked(interaction, self)

        button.callback = callback
        self.view.add_item(button)

    def prepare_category_select(self):
        options = []
        for category in self.categories:
            if category.is_null:
                options.append(discord.SelectOption(label=category.name,
                                                    value=category.id, default=True))
            else:
                options.append(discord.SelectOption(label=category.name,
                                                    value=category.id))

        select = Select(options=options)

        async def callback(interaction):
            await self.controller.on_category_select(interaction, select, self)

        select.callback = callback

        self.view.add_item(select)

    async def display(self, channel):
        await channel.send(content=f"link: {self.submission.link}", view=self.view)
