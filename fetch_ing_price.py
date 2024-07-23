#!/usr/bin/env python3

from datetime import datetime
from collections import deque
import argparse
import json
import os
import requests
import sys

def ing_url(chart, exchangeId, currencyId, timerange):
    url = "https://component-api.wertpapiere.ing.de/api/v1/charts/shm/{}?timeRange={}&exchangeId={}&currencyId={}".format(chart, timerange, exchangeId, currencyId)
    return url

DataPoint = lambda **kwargs: type("Object", (), kwargs)

def prices_ing(our_name, chart, exchangeId, currencyId, timerange='Intraday'):
    url = ing_url(chart, exchangeId, currencyId, timerange)
    reply = requests.get(url)

    try:
        data = json.loads(reply.text)

    except:
        print("Cannot load JSON for {}".format(url), file=sys.stderr)
        return

    visited_dates = set()
    outdata = []
    last_data_point = next(iter(deque(data["instruments"][0]["data"], 1)))

    try:
        # I am ugly, but I work
        date = datetime.fromtimestamp(float(last_data_point[0]) / 1e3).strftime("%Y-%m-%d")
    except:
        print("Cannot convert to date: {}".format(last_data_point[0]), file=sys.stderr)
        return

    price = last_data_point[1]
    return DataPoint(date = date, our_name = our_name, price = price)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fetch_ing_price",
        description=""
    )
    parser.add_argument(
        "--shortname", action="store",
    )
    parser.add_argument(
        "--chart", action="store",
    )
    parser.add_argument(
        "--exchange-id", action="store",
    )
    parser.add_argument(
        "--currency-id", action="store",
    )

    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()

    price = prices_ing(args.shortname, args.chart, args.exchange_id, args.currency_id)

    j = {}
    j["date"] = price.date
    j["shortname"] = args.shortname
    j["our_name"] = price.our_name
    j["price"] = price.price

    print(json.dumps(j))

if __name__ == "__main__":  # pragma: no cover
    main()
