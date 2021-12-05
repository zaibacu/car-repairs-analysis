import csv
import requests
from argparse import ArgumentParser

ROOT_URL = "https://www.warrantywise.co.uk/car-warranty/repairs/models"


def main(args):
    total_pages = 1
    current_page = 1

    csvfile = open(f"data/{args.make.upper()}.csv", "w")

    fieldnames = ['make', 'model', 'part', 'total_paid']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    while current_page <= total_pages:
        result = requests.get(f"{ROOT_URL}/{args.make}?page={current_page}")
        data = result.json()
        total_pages = int(data["last_page"])
        if isinstance(data["data"], list):
            items = data["data"]
        elif isinstance(data["data"], dict):
            items = [v for k, v in data["data"].items()]

        for item in items:
            writer.writerow({
                "make": item["car_make"],
                "model": item["car_model"],
                "part": item["part_repaired"],
                "total_paid": item["total_paid"]
            })
        current_page += 1

    csvfile.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("make", default="Car make to scrape")
    main(parser.parse_args())
