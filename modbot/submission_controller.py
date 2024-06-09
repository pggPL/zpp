import logging

import discord
from asgiref.sync import sync_to_async

from modbot.load_more_view import LoadMoreView
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

        # tells how many done submissions and pending submissions load at init
        self.n_submissions_shown_at_init = 2

    # loads content from db
    # and renders on the channels, assumes that given channels are already cleared
    async def init_from_db(self):

        # load categories - must happen before displaying submissions
        self.categories = await get_categories_from_db()

        # make db operations using a wrapper and convert to lists
        pending_submissions = await db(lambda: list(Submission.objects.filter(done=False)))
        done_submissions = await db(lambda: list(Submission.objects.filter(done=True)))

        # load submissions from db and display them
        # submissions = await get_submissions_from_db()

        # show only part of submissions during init
        for s in pending_submissions[:self.n_submissions_shown_at_init]:
            await self.add_submission(s)

        for s in done_submissions[:self.n_submissions_shown_at_init]:
            await self.add_submission(s)

        load_more_view = LoadMoreView(self)
        await load_more_view.display(self.pending_channel)

    async def update_view(self, submission: Submission):
        # find the view with id of edited submission
        submission_view = self.views.get(submission.id)

        # If the view was found, update it
        if submission_view is not None:
            await submission_view.update(submission)



    async def add_submission(self, submission: Submission):

        # use submission id as view id
        view_id = submission.id
        curr_category = await get_submission_category(submission)

        # display
        if submission.done:
            view = DoneSubmissionView(submission, self, view_id)
            channel = self.done_channel
        else:
            view = PendingSubmissionView(submission, curr_category, self, view_id)
            channel = self.pending_channel
        await view.display(channel)
        # add to internal structure
        self.views[view_id] = view

    # Events

    async def on_load_more_clicked(self, interaction: discord.Interaction):
        pending_submissions = \
            await db(lambda: list(Submission.objects.filter(done=False)))

        # finish with no response
        await interaction.response.defer()
        # delete the message that sent the interaction
        await interaction.message.delete()

        # filtered out these already showed
        filtered = list(filter
                        (lambda s: s.id not in self.views.keys(),
                         pending_submissions)
                        )

        for sub in filtered[:self.n_submissions_shown_at_init]:
            await self.add_submission(sub)

        # show new load more view after new submissions are loaded
        load_more_view = LoadMoreView(self)
        await load_more_view.display(self.pending_channel)

    async def on_done_clicked(self, interaction: discord.Interaction,
                              view: PendingSubmissionView):
        # update database
        await mark_as_done_in_db(view.submission)

        # finish with no response
        await interaction.response.defer()
        # delete the message that sent the interaction
        await interaction.message.delete()

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
