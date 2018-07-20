import json

import requests


def gbfs():
    """Fetches feed data from Bike Share Toronto's General Bike Share Feed 
    Specification.
    """
    GBFS_FEED = "https://tor.publicbikesystem.net/ube/gbfs/v1/"
    feed_spec = requests.get(GBFS_FEED)
    return json.loads(feed_spec.text)
