import logging

import discord
from asgiref.sync import sync_to_async

from modbot.pending_submission_view import PendingSubmissionView
from modbot.done_submission_view import DoneSubmissionView

from app_main.models import Submission, SubmissionCategory

from modbot.async_db_client import *


class SubmissionsController:

    def __init__(self, pending_channel: discord.TextChannel, done_channel: discord.TextChannel):
        self.pending_channel = pending_channel
        self.done_channel = done_channel

        # maps view_id to View
        self.views = {}
        self.categories = []

        self.n_submissions_shown_at_init = 10

    # loads content from db
    # and renders on the channels, assumes that given channels are already cleared
    async def init_from_db(self):

        # load categories - must happen before displaying submissions
        self.categories = await get_categories_from_db()

        # load submissions from db and display them
        submissions = await get_submissions_from_db()

        # show only part of submissions during init
        for s in submissions[:self.n_submissions_shown_at_init]:
            await self.add_submission(s)

    async def add_submission(self, submission: Submission):

        # use submission id as view id
        view_id = submission.id

        # display
        if submission.done:
            view = DoneSubmissionView(submission, self, view_id)
            channel = self.done_channel
        else:
            view = PendingSubmissionView(submission, self, view_id)
            channel = self.pending_channel
        await view.display(channel)
        # add to internal structure
        self.views[view_id] = view

    # Events
    async def on_done_clicked(self, interaction: discord.Interaction,
                              view: PendingSubmissionView):
        # update database
        await mark_as_done_in_db(view.submission)

        # finish interaction
        await interaction.response.edit_message(content="done", view=None)

        # delete pending submission view and add done submission view and render it
        view_id = view.view_id

        # the key really should be there
        del self.views[view_id]

        # make done view with the same id as deleted view
        new_view = DoneSubmissionView(view.submission, self, view_id)
        self.views[view_id] = new_view

        # render on done channel
        await new_view.display(self.done_channel)

    async def on_category_select(self, interaction, select, view: PendingSubmissionView):
        await change_submission_category_in_db(view.submission,
                                               category_id=select.values[0])
        await interaction.response.defer()

