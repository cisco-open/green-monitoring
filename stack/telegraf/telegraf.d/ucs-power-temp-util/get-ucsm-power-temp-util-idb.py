#!/usr/bin/env python

"""Script for retrieving power, temperature and utilization information
for UCSM servers.

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

__author__ = "Jean-Baptiste Lefeuvre <jlefeuvr@cisco.com>"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Apache License, Version 2.0"

import json
import pytz
import yaml
import multiprocessing
from datetime import datetime
from ucsmsdk.ucshandle import UcsHandle

# List of class IDs to be pulled from UCS
class_ids = ["EquipmentPsuInputStats", "ComputeMbPowerStats", "equipmentChassisStats"]

domains_file = "/etc/telegraf/telegraf.d/ucs-power-temp-util/ucsm-domains.yml"
credentials_file = "/etc/telegraf/telegraf.d/ucs-power-temp-util/ucsm-credentials.yml"
username = ""
password = ""


def get_ucs_domains():
    """
    update the ucs_domains variable with the list of ucs domains from ucsm-domains.yaml

    Parameters:
    None

    Returns:
    none

    list of ucs_domains formated like this:
    [(<domain1_name>, <domain1_ip), (<domain1_name>, <domain2_ip)]

    """

    global credentials_file, ucs_domains, username, password

    credentials = yaml.load(open(credentials_file), Loader=yaml.Loader)
    username = credentials["ucs_domains"]["username"]
    password = credentials["ucs_domains"]["password"]

    ucs_domains = list(
        yaml.load(open(domains_file), Loader=yaml.Loader)["ucs_domains"].items()
    )


def retrieve_data(ucs_domain):
    collection = []
    time = datetime.now().astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    try:
        handle = UcsHandle(ucs_domain[1], username, password)
        handle.login()
        raw_stats = handle.query_classids(class_ids)
        handle.logout()
        for class_id, obj_list in raw_stats.items():
            if class_id == "EquipmentPsuInputStats":
                # we collect FI power stats
                fi_json = {
                    # Assume UTC timezone
                    "time": time,
                    "domain-name": ucs_domain[0],
                    "domain-ip": ucs_domain[1],
                    "measurement": "ucsm-fabric-interconnect-power",
                    "fi-a-power": 0,
                    "fi-b-power": 0,
                    "fi-a-power-psu1": 0,
                    "fi-a-power-psu2": 0,
                }
                for obj in obj_list:
                    if "A" in obj.dn:
                        fi_json["fi-a-power"] = fi_json["fi-a-power"] + int(
                            obj.power.split(".")[0]
                        )
                        if "1" in obj.dn:
                            fi_json["fi-a-power-psu1"] = int(obj.power.split(".")[0])
                        elif "2" in obj.dn:
                            fi_json["fi-a-power-psu2"] = int(obj.power.split(".")[0])
                    elif "B" in obj.dn:
                        fi_json["fi-b-power"] = fi_json["fi-b-power"] + int(
                            obj.power.split(".")[0]
                        )
                        if "1" in obj.dn:
                            fi_json["fi-b-power-psu1"] = int(obj.power.split(".")[0])
                        elif "2" in obj.dn:
                            fi_json["fi-b-power-psu2"] = int(obj.power.split(".")[0])
                collection.append(fi_json)
            elif class_id == "ComputeMbPowerStats":
                # we collect ucsm server power stats
                for obj in obj_list:
                    server_json = {
                        # Assume UTC timezone
                        "time": time,
                        "domain-name": ucs_domain[0],
                        "domain-ip": ucs_domain[1],
                        "measurement": "ucsm-server-power",
                    }
                    if "blade" in obj.dn:
                        server_json["type"] = "blade"
                        server_json["chassis"] = obj.dn.split("/")[1]
                        server_json["id"] = obj.dn.split("/")[2]

                    elif "rack" in obj.dn:
                        server_json["type"] = "rack"
                        server_json["id"] = obj.dn.split("/")[1]
                    server_json["power"] = int(obj.consumed_power.split(".")[0])
                    collection.append(server_json)
            elif class_id == "EquipmentChassisStats":
                # we collect chassis power stats
                for obj in obj_list:
                    chassis_json = {
                        # Assume UTC timezone
                        "time": time,
                        "domain-name": ucs_domain[0],
                        "domain-ip": ucs_domain[1],
                        "measurement": "ucsm-chassis-power",
                    }
                    chassis_json["id"] = obj.dn.split("/")[1]
                    chassis_json["input-power"] = int(obj.input_power.split(".")[0])
                    chassis_json["output-power"] = int(obj.output_power.split(".")[0])
                    collection.append(chassis_json)
    except Exception as e:
        print(e)
    return collection


if __name__ == "__main__":

    get_ucs_domains()
    with multiprocessing.Pool(processes=4) as p:
        collections = p.map(retrieve_data, ucs_domains)
    flat_collection = [item for collection in collections for item in collection]
    print(json.dumps(flat_collection))
