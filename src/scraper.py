import json
from datetime import datetime
from time import sleep, time

import numpy as np
import pandas as pd
import requests


def get_gbfs():
    """Fetches feed data from Bike Share Toronto's GBFS API."""
    gbfs_data = dict()
    GBFS_FEED = "https://tor.publicbikesystem.net/ube/gbfs/v1/"
    feed_spec = requests.get(GBFS_FEED)
    feed_data = json.loads(feed_spec.text)
    gbfs_data["last_updated"] = feed_data["last_updated"]
    gbfs_data["ttl"] = feed_data["ttl"]
    for feed in feed_data["data"]["en"]["feeds"]:
        gbfs_data[feed["name"]] = feed["url"]
    return gbfs_data


def pull_station_information(gbfs_data):
    """Fetches all station information using the "station information" GBFS API."""
    raw_station_information = json.loads(
        requests.get(gbfs_data["station_information"]).text
    )["data"]["stations"]
    return {
        station["station_id"]: {
            "name": station["name"],
            "lat": station["lat"],
            "lon": station["lon"],
            "address": station["address"],
            "capacity": station["capacity"],
        }
        for station in raw_station_information
    }


def pull_station_status(gbfs_data):
    """Fetches the status of each station using the "station status" GBFS API."""
    station_status = dict()
    raw_station_status = json.loads(requests.get(gbfs_data["station_status"]).text)
    for station in raw_station_status["data"]["stations"]:
        station_status[(station["station_id"], "b_avail")] = station[
            "num_bikes_available"
        ]
        station_status[(station["station_id"], "b_dis")] = station["num_bikes_disabled"]
        station_status[(station["station_id"], "d_avail")] = station[
            "num_docks_available"
        ]
        station_status[(station["station_id"], "d_dis")] = station["num_docks_disabled"]
    return pd.DataFrame(
        station_status,
        index=[datetime.fromtimestamp(raw_station_status["last_updated"])],
    )


def pull(gbfs_data):
    station_status = pull_station_status(gbfs_data)
    return pd.DataFrame.from_dict(station_status)


def build_table(gbfs_data):
    station_information = pull_station_information(gbfs_data)
    return pd.DataFrame.from_dict(station_information)


def scrape_time_series(hour, minute, day, month, year):
    if any(arg is None for arg in [day, month, year]):
        t = datetime.now()
        if day is None:
            day = t.day
        if month is None:
            month = t.month
        if year is None:
            year = t.year
    print("Scraping up to", datetime(year, month, day, hour, minute), "...")
    dataset = pull(get_gbfs())
    cache_data(dataset, write_headers=True)
    sleep(30 - time() % 30)
    while datetime.now() < datetime(year, month, day, hour, minute):
        next_pull = pull(get_gbfs())
        cache_data(next_pull)
        dataset = pd.concat([dataset, next_pull])
        print("Scraped:", datetime.now())
        sleep(30 - time() % 30)
    return dataset


def cache_data(data, write_headers=False):
    if write_headers:
        data.to_csv("./data/cache.csv", mode="w")
    else:
        data.to_csv("./data/cache.csv", mode="a", header=False)
