#!/usr/bin/env python

"""Script for retrieving total PoE information for Meraki switches.

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

__author__ = "Oren Brigg <obrigg@cisco.com>"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Apache License, Version 2.0"

import asyncio
import json
from datetime import datetime

import meraki
import meraki.aio
import pytz

# Replace with your API key
api_key = "sample-api-key"
# Replace with your organization ID
org_id = "sample-organization-id"

timespan = 3600  # 3600 seconds = 1 hour
results = []

# Collect total PoE power usage for each switch
async def get_switches_power(switch_list):
    async with meraki.aio.AsyncDashboardAPI(
        api_key=api_key,
        output_log=False,
        suppress_logging=True,
        maximum_concurrent_requests=5,
        wait_on_rate_limit=True,
        nginx_429_retry_wait_time=2,
        maximum_retries=100,
    ) as aiomeraki:
        get_power_task = []
        for switch in switch_list:
            if switch["networkId"] != None:
                get_power_task.append(
                    async_get_switch(aiomeraki, switch["serial"], switch["name"])
                )
                get_power_task.append(
                    async_get_org(aiomeraki)
                )

        for task in asyncio.as_completed(get_power_task):
            await task


# Collect total switches power for an organisation
async def async_get_org(aiomeraki: meraki.aio.AsyncDashboardAPI):
    power = 0
    try:
        org_power = await aiomeraki.organizations.getOrganizationSummaryTopSwitchesByEnergyUsage(
            org_id, timespan=timespan
        )
        power = org_power[0]["usage"]["total"]
    except Exception as e:
        print(f"Some other ERROR: {e}")
    results.append(
        {
            # Assume UTC timezone
            "time": datetime.now()
            .astimezone(pytz.utc)
            .strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "org_id": org_id,
            "power": round(power),
        }
    )


# Collect total PoE power usage for a switch
async def async_get_switch(
    aiomeraki: meraki.aio.AsyncDashboardAPI, serial: str, name: str
):
    poe = 0
    try:
        switch_ports = await aiomeraki.switch.getDeviceSwitchPortsStatuses(
            serial, timespan=timespan
        )
        for port in switch_ports:
            if "powerUsageInWh" in port.keys():
                poe += port["powerUsageInWh"]
    except Exception as e:
        print(f"Some other ERROR: {e}")
    results.append(
        {
            # Assume UTC timezone
            "time": datetime.now()
            .astimezone(pytz.utc)
            .strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "org_id": org_id,
            "switch_serial": serial,
            "switch_name": name,
            "power": round(poe), # Units are in Wh
        }
    )


# Initialize Meraki API
dashboard = meraki.DashboardAPI(api_key=api_key, suppress_logging=True)

# Get the list of switches
switch_list = dashboard.organizations.getOrganizationInventoryDevices(
    org_id, productTypes=["switch"]
)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_switches_power(switch_list))

print(json.dumps(results))
