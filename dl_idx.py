#!/bin/python
import argparse
import csv
import os

import pandas as pd
import requests

user_agent = {
    "User-Agent": "07903619@company.com",
    "Accept-Encoding": "gzip, deflate",
    "Host": "www.sec.gov",
}


def process_quarterly():
    with open("full_index.csv", "w", newline="", encoding="utf-8") as csvfile:
        wr = csv.writer(csvfile)
        wr.writerow(["cik", "company_name", "form", "date", "url"])

        for year in range(1994, 2026):  # Adjust the range as needed
            for q in range(1, 5):
                print(f"Downloading {year} QTR{q}...")
                url = f"https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{q}/master.idx"
                try:
                    response = requests.get(url, headers=user_agent, stream=True)
                    response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)

                    # Process content line by line to save memory
                    for line in response.iter_lines(decode_unicode=True):
                        if line and ".txt" in line:
                            # Decode the line and split it
                            decoded_line = line.strip()
                            if decoded_line:
                                wr.writerow(decoded_line.split("|"))
                except requests.exceptions.RequestException as e:
                    print(f"Failed to download {year} QTR{q}: {e}")


if __name__ == "__main__":
    process_quarterly()
