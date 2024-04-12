import openpyxl


def read_file(file):
    workbook = openpyxl.load_workbook(file)
    worksheet = workbook.active

    data = []
    for row in worksheet.iter_rows(min_row=2, max_col=2, values_only=True):
        platform, link = row
        if platform is None or link is None:
            break
        data.append(row)

    return data

