#!/usr/bin/env python3

from datetime import datetime
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
    for data_point in data["instruments"][0]["data"]:
        try:
            # I am ugly, but I work
            date = datetime.fromtimestamp(float(data_point[0]) / 1e3).strftime("%Y-%m-%d")
        except:
            print("Cannot convert to date: {}".format(data_point[0]), file=sys.stderr)
            return

        if date in visited_dates:
            continue
        visited_dates.add(date)

        price = data_point[1]
        outdata.append(DataPoint(date = date, our_name = our_name, price = price))

    return outdata


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fetch.py",
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

def __main__():
    parser = init_argparse()
    args = parser.parse_args()

    prices = prices_ing(args.shortname, args.chart, args.exchange_id, args.currency_id)

    for price in prices:
        j = {}
        j["date"] = price.date
        j["shortname"] = args.shortname
        j["our_name"] = price.our_name
        j["price"] = price.price
        print(json.dumps(j))
