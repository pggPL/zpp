import openpyxl
from app_main.models import Platform, Submission

def read_links_file(file):
    workbook = openpyxl.load_workbook(file)
    worksheet = workbook.active

    data = []
    for row in worksheet.iter_rows(min_row=2, max_col=2, values_only=True):
        platform, link = row
        if platform is None or link is None:
            break
        data.append({"platform": platform, "link": link})

    return data


def save_to_db(data):
    for row in data:
        platform, link = row

        # FIXME: maybe we should add submission quantity to count submissions with the same link?
        # check if link already exists in database
        if Submission.objects.filter(link=link).exists():
            continue

        platform = Platform.objects.get_or_create(name=platform)[0]

        # create link in database
        Submission.objects.get_or_create(link=link, platform=platform)

