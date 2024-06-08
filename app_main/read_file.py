import openpyxl
from app_main.models import Platform, Submission, SubmissionCategory, ProfileSubmission
import re


def read_links_file(file):
    workbook = openpyxl.load_workbook(file)
    worksheet = workbook.active

    new_data = []
    other_data = []
    new_profile_data = []
    other_profile_data = []
    for row in worksheet.iter_rows(min_row=2, max_col=2, values_only=True):
        platform, link = row
        if platform is None or link is None:
            break

        dict_row = {"platform": platform, "link": link}

        if is_profile(link):
            if dict_row in new_profile_data or ProfileSubmission.objects.filter(link=link).exists():
                other_profile_data.append(dict_row)
            else:
                new_profile_data.append(dict_row)
        elif dict_row in new_data or Submission.objects.filter(link=link).exists():
            other_data.append(dict_row)
        else:
            new_data.append(dict_row)

    return new_data, other_data, new_profile_data, other_profile_data


def save_to_db(data):
    for row in data["posts"]:
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
    
    for row in data["profiles"]:
        platform = row["platform"]
        link = row["link"]

        platform = Platform.objects.get_or_create(name=platform)[0]

        # create link in database
        ProfileSubmission.objects.get_or_create(link=link, platform=platform)


def is_profile(url: str) -> bool:
    return is_facebook_profile(url) or is_twitter_profile(url)


def is_facebook_profile(url: str) -> bool:
    # This pattern matches most popular profile url
    pattern = r'https?://(www\.)?facebook\.com/profile\.php\?id=([0-9]+)(&comment_id=[a-zA-Z0-9%]+)?/?'

    # This pattern matches where after .com/ there is a profile name
    pattern2 = r'https?://(www\.)?facebook\.com/[a-zA-Z0-9\.]+(\?comment_id=[a-zA-Z0-9%]+)?/?'

    return bool(re.fullmatch(pattern, url)) or bool(re.fullmatch(pattern2, url))


def is_twitter_profile(url: str) -> bool:
    # Twitter profile names must contain between 1-15 alfa-numeric characters
    pattern = r'https?://(www\.)?(twitter|x)\.com/([a-zA-Z0-9_]{1,15})/?'

    return bool(re.fullmatch(pattern, url))
