#!/usr/bin/env python

"""Script for retrieving power information for nodes of the ACI APIC.

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
import re
import pytz
import json
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

apics = {"apic0.domain.com": ""}
nodes = {"3331": {}, "3332": {}}
username = "user"
password = "fgklfgkfl"


def get_call(apic, token, call):
    cookie = {"APIC-cookie": token}
    r_nodes_json = requests.get(
        "https://" + apic + call, cookies=cookie, verify=False
    ).json()

    return r_nodes_json


def read_power(node):
    node[1]["collection"] = []
    psu_nrs = range(0, 10)

    for psu_nr in psu_nrs:
        r_power_json = get_call(
            node[1]["apic"],
            apics[node[1]["apic"]],
            "/api/node/mo/topology/pod-1/node-"
            + node[0]
            + "/sys/pie/env/psu-"
            + str(psu_nr)
            + "/psu_power_info.json?query-target=self",
        )

        if (
            r_power_json
            and "totalCount" in r_power_json
            and int(r_power_json["totalCount"]) > 0
        ):
            for i in range(0, int(r_power_json["totalCount"])):
                psu_id = re.search(
                    "psu-.*/psu_power_info",
                    r_power_json["imdata"][i]["piePsuPowerInfo"]["attributes"]["dn"],
                ).group(0)[0:-15]

                body = {
                    # Assume UTC timezone
                    "time": datetime.now()
                    .astimezone(pytz.utc)
                    .strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    "dn": node[1]["dn"],
                    "id": node[1]["id"],
                    "name": node[1]["name"],
                    "role": node[1]["role"],
                    "model": node[1]["model"],
                    "serial": node[1]["serial"],
                    "address": node[1]["address"],
                    "apic": node[1]["apic"],
                    "psu_id": psu_id,
                    "pIn": float(
                        r_power_json["imdata"][i]["piePsuPowerInfo"]["attributes"][
                            "pIn"
                        ]
                    ),
                    "pOut": float(
                        r_power_json["imdata"][i]["piePsuPowerInfo"]["attributes"][
                            "pOut"
                        ]
                    ),
                }

                node[1]["collection"].append(body)


def create_nodes(apic):
    r_nodes_json = get_call(apic[0], apic[1], "/api/node/class/fabricNode.json")

    # Search for node names
    for d in r_nodes_json["imdata"]:
        n_id = d["fabricNode"]["attributes"]["id"]
        if n_id in nodes:
            nodes[n_id]["time"] = (
                datetime.now().astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
            )
            nodes[n_id]["dn"] = d["fabricNode"]["attributes"]["dn"]
            nodes[n_id]["id"] = d["fabricNode"]["attributes"]["id"]
            nodes[n_id]["name"] = d["fabricNode"]["attributes"]["name"]
            nodes[n_id]["role"] = d["fabricNode"]["attributes"]["role"]
            nodes[n_id]["model"] = d["fabricNode"]["attributes"]["model"]
            nodes[n_id]["serial"] = d["fabricNode"]["attributes"]["serial"]
            nodes[n_id]["address"] = d["fabricNode"]["attributes"]["address"]
            nodes[n_id]["apic"] = apic[0]


def get_token(apic):
    r_json = requests.post(
        "https://" + apic + "/api/aaaLogin.json",
        json={"aaaUser": {"attributes": {"name": username, "pwd": password}}},
        verify=False,
    ).json()

    token = r_json["imdata"][0]["aaaLogin"]["attributes"]["token"]

    return token


# Do not use proxy for the apics
# Disable this in case proxy was preset and is needed
os.environ["no_proxy"] = ",".join(apics)

# Get authorization tokens
for apic in apics.items():
    apics[apic[0]] = get_token(apic[0])

# Get nodes
for apic in apics.items():
    create_nodes(apic)

# Request power information for each node
for node in nodes.items():
    read_power(node)

flat_collection = [item for node in nodes.items() for item in node[1]["collection"]]

print(json.dumps(flat_collection))
