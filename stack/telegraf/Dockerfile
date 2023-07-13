# Dockerfile for data collector.
#
# Copyright (c) 2022 Cisco and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# AUTHOR(s): Cristina Precup <cprecup@cisco.com>
# CONTRIBUTOR(s): Steven Barth <stbarth@cisco.com>

FROM telegraf:1.24-alpine

ARG http_proxy=$HTTPS_PROXY \
    env_pip_requirements="/requirements.txt"

RUN apk add python3 py3-pip curl
COPY snmp/* /usr/share/snmp/mibs/
ADD requirements.txt $env_requirements

# Python dependencies
RUN if [ -z "$HTTPS_PROXY" ] ;\
    then pip3 install --upgrade pip && pip3 install -r $env_pip_requirements;\
    else pip3 install --proxy $HTTPS_PROXY --upgrade pip && pip3 install --proxy $HTTPS_PROXY -r $env_pip_requirements;\
    fi
# Eaton dependencies
RUN if [ -z "$HTTPS_PROXY" ] ;\
    then curl --max-time 30 --user-agent 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.1a) Gecko/20020619' https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/Firmware/eaton-pdu-g3-firmware-mib.zip --output eaton-pdu-g3-firmware-mib.zip;\
    else curl --proxy $HTTPS_PROXY --max-time 30 --user-agent 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.1a) Gecko/20020619' https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/Firmware/eaton-pdu-g3-firmware-mib.zip --output eaton-pdu-g3-firmware-mib.zip;\
    fi;\
    unzip eaton-pdu-g3-firmware-mib.zip -d eaton-pdu-g3-firmware-mib && cd eaton-pdu-g3-firmware-mib && unzip EATON-EPDU-MIB.zip -d EATON-EPDU-MIB && mv EATON-EPDU-MIB/*-MIB.txt /usr/share/snmp/mibs/;\
    exit 0