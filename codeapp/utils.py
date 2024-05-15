# built-in imports
# standard library imports
import pickle

# external imports
from flask import current_app

# internal imports
from codeapp import db
from codeapp.models import our_class

import csv
import requests
import redis
from typing import List


def get_data_list() -> List[our_class]:
    url = "https://onu1.s2.chalmers.se/datasets/Europe_Sales_Records.csv"
    response = requests.get(url)
    data = response.text.split("\n")

    reader = csv.reader(data)
    headers = next(reader)
    data_list = [our_class(*row) for row in reader if len(row) == 9]

    r = redis.Redis(
        host="onu1.s2.chalmers.se",
        port=6380,
        db=92,
        password="a62b9a30-24a4-4153-a2a1-42d577161676",
    )
    for item in data_list:
        # Serialize the object
        serialized_item = pickle.dumps(item)
        # Store the serialized object in Redis
        r.lpush("dataset_list", serialized_item)

    return data_list


"""
Function responsible for downloading the dataset from the source, translating it
into a list of Python objects, and saving it to a Redis list.
"""

from collections import Counter
from datetime import datetime


def calculate_statistics(dataset: list) -> dict:
    """
    Receives the dataset in the form of a list of Python objects, and calculates the
    statistics necessary.
    """
    # Calculate the number of orders per transit day between 10 to 30
    transit_days_counter = Counter(
        (
            datetime.strptime(item.ship_date, "%m/%d/%Y")
            - datetime.strptime(item.order_date, "%m/%d/%Y")
        ).days
        for item in dataset
        if 10
        <= (
            datetime.strptime(item.ship_date, "%m/%d/%Y")
            - datetime.strptime(item.order_date, "%m/%d/%Y")
        ).days
        <= 30
    )

    return {
        "orders_per_transit_day": dict(transit_days_counter),
    }


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
