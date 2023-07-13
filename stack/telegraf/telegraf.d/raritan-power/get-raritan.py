#!/usr/bin/env python
 
"""Script for retrieving power information for Raritan PDUs.

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

import os, sys
import getopt
import pytz
import json
import yaml
import multiprocessing
from datetime import datetime

from raritan import rpc
from raritan.rpc import pdumodel

model = '/model/pdu/0'

# Before running this script: edit the raritan-credentials.yml file
# with the right credentials and the raritan-pdus.yml with the
# right list of Raritan PDUs

# Set default paths
pdus_file = '/etc/telegraf/telegraf.d/raritan-power/raritan-pdus.yml'
credentials_file = '/etc/telegraf/telegraf.d/raritan-power/raritan-credentials.yml'


def retrieve_data(data):
    collection = []
    name, ip = data
    name = model + '-' + name

    try:
        agent = rpc.Agent('https', ip, username, password) 
        pdu = pdumodel.Pdu(model, agent)
        metadata = pdu.getMetaData()

        # Get current, voltage, activePower, phaseAngle readings from inlets
        inlets = pdu.getInlets()
        for i in inlets:

            json_body = {
                'name': name,
                # Assume UTC timezone
                'time': datetime.now().astimezone(pytz.utc).
                                    strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                'current': i.getSensors().current.getReading().value, # A
                'unbalancedCurrent': i.getSensors().unbalancedCurrent.getReading().value, # %
                'voltage': i.getSensors().voltage.getReading().value, # V
                'activePower': i.getSensors().activePower.getReading().value/1000, # kW
                'apparentPower': i.getSensors().apparentPower.getReading().value/1000, # kVA
                'activeEnergy': i.getSensors().activeEnergy.getReading().value/1000000, # MWh
                'lineFrequency': i.getSensors().lineFrequency.getReading().value # Hz
            }

            collection.append(json_body)

    except Exception as e:
        print(e)
        
    return collection

def main(argv):
    global pdus_file, credentials_file, raritan_pdus, username, password

    try:
        opts, args = getopt.getopt(argv,"p:c:",["pdusyml=","credentialsyml="])
    except getopt.GetoptError:
        print('get-raritan.py -p <pdusyml> -c <credentialsyml>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--pdusyml"):
            pdus_file = arg
        elif opt in ("-c", "--credentialsyml"):
            credentials_file = arg

    credentials = yaml.load(
                open(credentials_file), 
                Loader=yaml.Loader)
    username = credentials['pdu']['username']
    password = credentials['pdu']['password']

    pdus = yaml.load(
                open(pdus_file),
                Loader=yaml.Loader)
    raritan_pdus = pdus['pdus']

    # Do not use proxy for the Raritan IP addresses
    # Disable this in case proxy was preset and is needed
    os.environ['no_proxy'] = ','.join(list(raritan_pdus.values()))


if __name__ == '__main__':
    main(sys.argv[1:])

    with multiprocessing.Pool(processes=4) as p:
        collections = p.map(retrieve_data, raritan_pdus.items())
    flat_collection = [item for collection in collections for item in collection]

    print(json.dumps(flat_collection))
