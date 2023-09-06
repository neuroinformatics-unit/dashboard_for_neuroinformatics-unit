"""
Functions to get download data from pypi
"""
import subprocess
from datetime import datetime
from pypinfo.cli import pypinfo


def get_existing_data(packagename, data_path="libraries/pypi-downloads/"):
    """
    Looks for text files in data_path that match the package name
    and returns the data in them
    """
    filename = str(data_path + packagename + ".downloads")
    months = []
    downloads = []
    try:
        with open(filename, "r") as filein:
            for line in filein.readlines():
                if line[0] != "#":
                    months.append(line.split()[0])
                    downloads.append(line.split()[1])
    except FileNotFoundError:
        pass

    return months, downloads


def get_missing_months(start_month, existing_months):
    """
    Starts from start_month and looks for any months up to the current month -1
    that are not in the data and returns a list of missing months
    """
    month = int(start_month[-2:])
    year = int(start_month[:4])

    current_date = datetime.today()
    current_month = current_date.month
    current_year = int(current_date.year)

    missing_months = []
    year_month_format = "{year:4d}-{month:02d}"
    while year <= current_year:
        end_month = 12
        if year == current_year:
            end_month = current_month - 1
        while month <= end_month:
            year_month = year_month_format.format(year=year, month=month)
            if year_month not in existing_months:
                missing_months.append(year_month)
            month += 1
        month = 1
        year += 1

    return missing_months


def query_new_data(packagename, month, include_mirrors=False):
    subprocess.run(["pypinfo", "--auth", "snappy-downloads-3d3fb7e245fd.json"])
    download = subprocess.run(
        ["pypinfo", "--month", month, packagename], capture_output=True
    ).stdout
    return download.decode("utf-8")


if __name__ == "__main__":
    months, downloads = get_existing_data("ndicapi")

    for i, month in enumerate(months):
        print("month: ", month, " Downloads: ", downloads[i])

    missing_months = get_missing_months("2019-01", months)
    print("querying ", missing_months[0])
    new_data = query_new_data("ndicapi", missing_months[0])
    new_data_by_line = new_data.splitlines()

    downloads = int(new_data_by_line[7].replace("|", "").replace(" ", ""))
    print("Downloads = ", downloads)
    for i, line in enumerate(new_data_by_line):
        print(i, " of ", len(new_data_by_line), ":", line)
