from typing import Callable

from app_main.models import Submission, SubmissionCategory
from asgiref.sync import sync_to_async
async def mark_as_done_in_db(submission: Submission):
    def db_action():
        submission.done = True
        submission.save()

    return await sync_to_async(db_action)()



async def get_submissions_from_db():
    def db_action():
        return list(Submission.objects.all())

    return await sync_to_async(db_action)()


async def get_categories_from_db():
    def db_action():
        return list(SubmissionCategory.objects.all())

    return await sync_to_async(db_action)()


async def change_submission_category_in_db(submission: Submission, category_id: int):
    def db_action():
        submission.category = SubmissionCategory.objects.get(id=category_id)
        submission.save()

    return await sync_to_async(db_action)()


async def get_submission_category(submission: Submission) -> SubmissionCategory:
    def db_action():
        return submission.category

    return await sync_to_async(db_action)()


# accepts no arguments action to be made on db
async def db(action: Callable):
    return await sync_to_async(action)()


