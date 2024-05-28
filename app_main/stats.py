from app_main.models import Submission, SubmissionCategory
from collections import defaultdict

def get_categories_dict():
    categories_dict = {category.name: len(Submission.objects.filter(category=category)) 
                       for category in SubmissionCategory.objects.all()}
    categories_dict.pop("brak kategorii", None)
    return categories_dict

def get_basic_date_dict():
    dates_dict = defaultdict(int)
    for submission in Submission.objects.all():
        date = submission.date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        dates_dict[date] += 1
    return dict(dates_dict)

def fill_missing_dates(dates_dict):
    first_date = min(dates_dict.keys())
    last_date = max(dates_dict.keys())
    current_date = first_date
    while current_date < last_date:
        current_date = current_date.replace(month=current_date.month + 1)
        if current_date not in dates_dict:
            dates_dict[current_date] = 0
    return dates_dict

def get_timechart_data():
    dates_dict = get_basic_date_dict()
    dates_dict = fill_missing_dates(dates_dict)
    res = []
    for date in dates_dict:
        res.append({
            "x": date.strftime("%Y-%m"),
            "y": dates_dict[date]
        })
    return res

