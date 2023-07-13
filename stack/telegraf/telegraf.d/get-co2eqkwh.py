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
import pytz
import json
import time
from datetime import datetime
import requests

session = requests.Session()

# Max 30 requests per hour

collection = []
countryCodes = ["DE", "ES", "FR", "IT-CNO", "IT-CSO", "IT-SO"]
url = "https://api.co2signal.com/v1/latest?countryCode="
headers = {'auth-token': os.environ['CO2_SIGNAL_TOKEN']}

for cc in countryCodes:
    response = session.get(url + cc, headers=headers)

    js = response.json()

    if cc == "DE":
        country = "Germany"
        region = "Bavaria"
    elif cc == "ES":
        country = "Spain"
        region = "Catalonia"
    elif cc == "FR":
        country = "France"
        region = "Auvergne-Rhône-Alpes"
    else:
        country = "Italy"
        if cc == "IT-CNO":
            region = "Central North"
        elif cc == "IT-CSO":
            region = "Central South"
        elif cc == "IT-SO":
            region = "South"

    if 'data' in js:

        # Check if data exists:
        if js['data']['fossilFuelPercentage']:
            json_body = {
                # Assume UTC timezone
                'time': datetime.now().astimezone(pytz.utc).
                                    strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                'acquired_time': js['data']['datetime'], # TODO
                'cc': cc,
                'country': country,
                'region': region,
                'unitCarbonIntensity': js['units']['carbonIntensity'],
                'fossilFuelPercentage': js['data']['fossilFuelPercentage'],
                'carbonIntensity': js['data']['carbonIntensity']
            }

            collection.append(json_body)
    time.sleep(1)

print(json.dumps(collection))
