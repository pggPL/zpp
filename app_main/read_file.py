import openpyxl
from app_main.models import Platform, Submission, SubmissionCategory
import re


def read_links_file(file):
    workbook = openpyxl.load_workbook(file)
    worksheet = workbook.active

    new_data = []
    other_data = []
    for row in worksheet.iter_rows(min_row=2, max_col=2, values_only=True):
        platform, link = row
        if platform is None or link is None:
            break

        dict_row = {"platform": platform, "link": link}

        if dict_row in new_data or Submission.objects.filter(link=link).exists():
            other_data.append(dict_row)
        else:
            new_data.append(dict_row)

    return new_data, other_data


def save_to_db(data):
    for row in data:
        platform = row["platform"]
        link = row["link"]

        # check if link already exists in database
        if Submission.objects.filter(link=link).exists():
            submission = Submission.objects.get(link=link)
            submission.report_count += 1
            submission.save()
            continue

        platform = Platform.objects.get_or_create(name=platform)[0]
        category = SubmissionCategory.objects.get_or_create(name="brak kategorii", is_null=True)[0]

        # create link in database
        Submission.objects.get_or_create(link=link, platform=platform, category=category)


def is_profile(url: str) -> bool:
    return is_facebook_profile(url) or is_twitter_profile(url)


def is_facebook_profile(url: str) -> bool:
    # This pattern matches most popular profile url
    pattern = r'https?://www\.facebook\.com/profile\.php\?id=([0-9]+)'

    # This pattern matches where after .com/ there is [first name].[last name]
    pattern2 = r'https?://www\.facebook\.com/[a-zA-Z]+\.[a-zA-Z]+'

    return bool(re.match(pattern, url)) or bool(re.match(pattern2, url))


def is_twitter_profile(url: str) -> bool:
    # Twitter profile names must contain between 1-15 alfa-numeric characters
    # and underscores and can't start with the digit
    # we assume that after '?' can be anything (which should be good enough)
    pattern = r'https?://(www\.)?twitter\.com([a-zA-Z_][a-zA-Z0-9_]{0,14})\?.*'

    return bool(re.match(pattern, url))
