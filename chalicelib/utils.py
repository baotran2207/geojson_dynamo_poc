import csv
import math


def get_page_info(num_results: list, page_num=1, results_per_page=3):
    if results_per_page > 0:
        start = max(0, min(num_results, (page_num - 1) * results_per_page))
        end = max(0, min(num_results, start + results_per_page))
        total_pages = int(math.ceil(float(num_results) / results_per_page))
    else:
        page_num = 1
        start = 0
        end = num_results
        total_pages = 1

    assert start >= 0 and end >= 0 and end >= start, [start, end]

    return (
        start,
        end,
        dict(page=page_num, num_results=num_results, total_pages=total_pages),
    )


def get_base_url(current_request):
    headers = current_request.headers
    base_url = "%s://%s" % (headers.get("x-forwarded-proto", "http"), headers["host"])
    if "stage" in current_request.context:
        base_url = "%s/%s" % (base_url, current_request.context.get("stage"))
    return base_url


def parse_csv_to_json(f_path) -> list:
    jsonArray = []

    # read csv file
    with open(f_path, encoding="utf-8") as csvf:
        # load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf)

        # convert each csv row into python dict
        for row in csvReader:
            # add this python dict to json array
            ## yield row
            jsonArray.append(row)

    return jsonArray
