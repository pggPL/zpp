import discord
from discord.ui import Button, View


class LoadMoreView:

    def __init__(self, controller):
        self.controller = controller
        self.view = View()

        self.prepare_load_more_button()

    def prepare_load_more_button(self):
        button = Button(label="load more", style=discord.ButtonStyle.blurple)

        async def callback(interaction: discord.Interaction):
            await self.controller.on_load_more_clicked(interaction)

        button.callback = callback
        self.view.add_item(button)

    async def display(self, channel):
        await channel.send("\u200B\n", view=self.view)
