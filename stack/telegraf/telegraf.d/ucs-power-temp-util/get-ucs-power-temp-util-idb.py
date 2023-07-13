#!/usr/bin/env python

"""Script for retrieving power, temperature and utilization information
for UCS servers.

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
import json
import pytz
import yaml
import multiprocessing
from datetime import datetime
from imcsdk.imchandle import ImcHandle
from imcsdk.imcconstants import NamingId
import sys, getopt

# Before running this script: edit the ucs-credentials.yml file
# with the right credentials and ucs-servers.yaml with
# the right list of UCS servers

# Set default paths
servers_file = "/etc/telegraf/telegraf.d/ucs-power-temp-util/ucs-servers.yml"
credentials_file = "/etc/telegraf/telegraf.d/ucs-power-temp-util/ucs-credentials.yml"

query_dns = {
    # Power
    "power_monitors": NamingId.POWER_MONITOR,
    "power_equipment_psus": NamingId.EQUIPMENT_PSU,
    # Temperature
    "compute_rack_unit_temp": NamingId.COMPUTE_RACK_UNIT_MB_TEMP_STATS,
    "memory_unit_temp": NamingId.MEMORY_UNIT_ENV_STATS,
    "processor_temp": NamingId.PROCESSOR_ENV_STATS,
    # Utilization
    "server_utilization": NamingId.SERVER_UTILIZATION,
}


def retrieve_data(data):
    name, ip = data
    collection = []
    try:
        with ImcHandle(ip, username, password) as handle:
            for qd_name, qd_id in query_dns.items():
                response = handle.query_classid(
                    class_id=qd_id, hierarchy=False, need_response=False
                )

                # Each uniquely identifiable resource gets a separate json
                # (Platform, CPU, Memory, PSU, temperature, utilization)
                for r in response:

                    json_body = {
                        # Assume UTC timezone
                        "time": datetime.now()
                        .astimezone(pytz.utc)
                        .strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        "name": name,
                        "ip": ip,
                    }

                    # Set measurement name
                    if "power" in qd_name:
                        json_body["measurement"] = "cimc-ucs-power"
                    elif "temp" in qd_name:
                        json_body["measurement"] = "cimc-ucs-temperature"
                    else:
                        json_body["measurement"] = "cimc-ucs-utilization"

                    # Power
                    if qd_name == "power_monitors":
                        json_body["domain"] = r.domain
                        if r.current and r.current != "N/A":
                            json_body["current_power"] = int(r.current)
                    elif qd_name == "power_equipment_psus":
                        json_body["psu-id"] = r.id
                        json_body["psu-pid"] = r.pid
                        if r.input and r.input != "N/A":
                            json_body["input"] = int(r.input)
                        if r.output and r.output != "N/A":
                            json_body["output"] = int(r.output)
                    # Temperature
                    elif qd_name == "compute_rack_unit_temp":
                        json_body["dn"] = r.dn
                        if r.ambient_temp and r.ambient_temp != "N/A":
                            json_body["ambient_temp"] = float(r.ambient_temp)
                        if r.front_temp and r.front_temp != "N/A":
                            json_body["front_temp"] = float(r.front_temp)
                        if r.rear_temp and r.rear_temp != "N/A":
                            json_body["rear_temp"] = float(r.rear_temp)
                    elif qd_name == "memory_unit_temp":
                        json_body["dn"] = r.dn
                        json_body["id"] = r.id
                        if r.temperature and r.temperature != "N/A":
                            json_body["temperature"] = float(r.temperature)
                    elif qd_name == "processor_temp":
                        json_body["dn"] = r.dn
                        json_body["id"] = r.id
                        if r.temperature and r.temperature != "N/A":
                            json_body["temperature"] = float(r.temperature)
                    # Utilization
                    elif qd_name == "server_utilization":
                        json_body["dn"] = r.dn
                        if r.io_utilization and r.io_utilization != "N/A":
                            json_body["io_utilization"] = float(r.io_utilization)
                        if r.cpu_utilization and r.cpu_utilization != "N/A":
                            json_body["cpu_utilization"] = float(r.cpu_utilization)
                        if r.memory_utilization and r.memory_utilization != "N/A":
                            json_body["memory_utilization"] = float(
                                r.memory_utilization
                            )
                        if r.overall_utilization and r.overall_utilization != "N/A":
                            json_body["overall_utilization"] = float(
                                r.overall_utilization
                            )

                    collection.append(json_body)
    except Exception as e:
        print(e)

    return collection


def main(argv):
    global servers_file, credentials_file, ucs_servers, username, password

    try:
        opts, args = getopt.getopt(argv, "s:c:", ["serversyml=", "credentialsyml="])
    except getopt.GetoptError:
        print("get-ucs-power-temp-util-idb.py -s <serversyml> -c <credentialsyml>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--serversyml"):
            servers_file = arg
        elif opt in ("-c", "--credentialsyml"):
            credentials_file = arg

    credentials = yaml.load(open(credentials_file), Loader=yaml.Loader)
    username = credentials["ucs"]["username"]
    password = credentials["ucs"]["password"]

    servers = yaml.load(open(servers_file), Loader=yaml.Loader)
    ucs_servers = servers["servers"]

    # Do not use proxy for the UCS server IP addresses
    # Disable this in case proxy was preset and is needed
    os.environ["no_proxy"] = ",".join(list(ucs_servers.values()))


if __name__ == "__main__":
    main(sys.argv[1:])

    with multiprocessing.Pool(processes=4) as p:
        collections = p.map(retrieve_data, ucs_servers.items())
    flat_collection = [item for collection in collections for item in collection]

    print(json.dumps(flat_collection))
