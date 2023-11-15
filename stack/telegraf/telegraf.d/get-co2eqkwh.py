#!/usr/bin/env python

"""Script for retrieving CO2 emissions / kWh.

Copyright (c) 2022 Cisco and/or its affiliates. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

__author__ = "Cristina Precup <cprecup@cisco.com>"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Apache License, Version 2.0"

import os
import sys
import pytz
import json
import time
import logging as log
from datetime import datetime
import requests

zones = ["DE", "ES", "FR", "IT-CNO", "IT-CSO", "IT-SO"]
url_emaps = "https://api.electricitymap.org/v3/carbon-intensity/latest?zone="
url_co2signal = "https://api.co2signal.com/v1/latest?countryCode="


def read_emaps(js, zone, country, region):
    # Check if data exists
    if "carbonIntensity" not in js:
        return None

    return base_json_body(js, zone, country, region)


def read_co2_signal(js, zone, country, region):
    # Check if data exists
    if "data" not in js:
        return None

    data = js["data"]

    if data["carbonIntensity"]:
        json_body = base_json_body(data, zone, country, region)
        json_body.update(
            {
                "unitCarbonIntensity": js["units"]["carbonIntensity"],
                "fossilFuelPercentage": data["fossilFuelPercentage"],
            }
        )
        return json_body
    return None


def base_json_body(data, zone, country, region):
    return {
        # Assume UTC timezone
        "time": datetime.now().astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "acquired_time": data["datetime"],  # TODO
        "cc": zone,
        "country": country,
        "region": region,
        "carbonIntensity": data["carbonIntensity"],
    }


if __name__ == "__main__":

    collection = []
    session = requests.Session()

    # Check if CO2_SIGNAL_TOKEN is set
    if "CO2_SIGNAL_TOKEN" in os.environ:
        headers = {"auth-token": os.environ["CO2_SIGNAL_TOKEN"]}
        url = url_co2signal

    # Check if EMAPS_TOKEN is set
    if "EMAPS_TOKEN" in os.environ:
        headers = {"auth-token": os.environ["EMAPS_TOKEN"]}
        url = url_emaps

    if "url" not in locals():
        sys.exit("ERROR: Token not set.")

    for zone in zones:
        response = session.get(url + zone, headers=headers)
        if response.status_code != 200:
            log.warning(str(response.status_code) + ": " + response.text)
            continue
        js = response.json()

        if zone == "DE":
            country = "Germany"
            region = "Bavaria"
        elif zone == "ES":
            country = "Spain"
            region = "Catalonia"
        elif zone == "FR":
            country = "France"
            region = "Auvergne-Rhône-Alpes"
        else:
            country = "Italy"
            if zone == "IT-CNO":
                region = "Central North"
            elif zone == "IT-CSO":
                region = "Central South"
            elif zone == "IT-SO":
                region = "South"

        if url == url_co2signal:
            # Get CO2 Signal data
            collection.append(read_co2_signal(js, zone, country, region))
        else:
            # Get EMAPS data
            collection.append(read_emaps(js, zone, country, region))

        time.sleep(1)

    print(json.dumps(collection))
