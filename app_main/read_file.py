import openpyxl
from app_main.models import Platform, Submission, SubmissionCategory

def read_links_file(file):
    workbook = openpyxl.load_workbook(file)
    worksheet = workbook.active

    new_data = []
    other_data = []
    for row in worksheet.iter_rows(min_row=2, max_col=2, values_only=True):
        platform, link = row
        if platform is None or link is None:
            break
        if {"platform": platform, "link": link} in new_data:
            other_data.append({"platform": platform, "link": link})
            continue
        if Submission.objects.filter(link=link).exists():
            other_data.append({"platform": platform, "link": link})
            continue

        new_data.append({"platform": platform, "link": link})

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


