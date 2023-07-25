# Prerequisites, Configuration and Installation

- [Prerequisites, Configuration and Installation](#prerequisites-configuration-and-installation)
  - [Prerequisites](#prerequisites)
    - [Host environment](#host-environment)
    - [Container platform](#container-platform)
  - [Configuration](#configuration)
    - [IOS-XR routers and NX-OS switches](#ios-xr-routers-and-nx-os-switches)
    - [Meraki switches](#meraki-switches)
    - [ACI APIC nodes](#aci-apic-nodes)
    - [UCSs](#ucss)
      - [REDFISH API](#redfish-api)
      - [CIMC API](#cimc-api)
      - [UCSM API](#ucsm-api)
    - [Raritan PDUs](#raritan-pdus)
    - [Eaton PDUs](#eaton-pdus)
    - [CO2-eq emissions](#co2-eq-emissions)
    - [Telemetry streaming](#telemetry-streaming)
  - [Installation](#installation)
    - [Create the stack of containers](#create-the-stack-of-containers)



## Prerequisites


### Host environment

Ubuntu 20.04 / 22.04, cloud image:

| VCPUs | Disk (in GB) | RAM (in MB) |
| :---: | -----------: | ----------: |
|   4   |           80 |        8192 |
|   8   |          160 |       16384 |


### Container platform

Install Docker, Docker-compose:

```bash
    cd installer

    bash 01.install-docker.sh

    # Optional
    sudo bash 02.setup-docker-dns.sh

    bash 03.install-docker-compose.sh
```
## Configuration

Configure environment and input data sources. Follow the format in the following files. For more details, see also the numbered sections below.

- Environment - see:
  - [.env](.env)
- Data enrichment: mapping geo (country, region, cc) and rack to devices - see:
  - [telegraf-mapping.conf](telegraf/telegraf.d/telegraf-mapping.conf)
- IOS-XR routers - see:
  - [Configure telemetry streaming](#configure-telemetry-streaming)
- NX-OS switches - see:
  - [Configure telemetry streaming](#configure-telemetry-streaming)
  - [telegraf/telegraf.d/apic/get-switch-power.py](telegraf/telegraf.d/apic/get-switch-power.py) lines #12-#15
- Meraki switches - see:
  - [telegraf/telegraf.d/meraki/get-meraki-power.py](telegraf/telegraf.d/meraki/get-meraki-power.py)
  - [telegraf/telegraf.d/telegraf-switch-meraki.conf](telegraf/telegraf.d/telegraf-switch-meraki.conf)
- UCS servers - see:
  - [telegraf/telegraf.d/telegraf-redfish.conf](telegraf/telegraf.d/telegraf-redfish.conf)
  - [telegraf/telegraf.d/telegraf-ucs-cimc.conf](telegraf/telegraf.d/telegraf-ucs-cimc.conf)
  - [telegraf/telegraf.d/telegraf-ucsm.conf](telegraf/telegraf.d/telegraf-ucsm.conf)
  - [telegraf/telegraf.d/ucs-power-temp-util/ucs-credentials.yml](telegraf/telegraf.d/ucs-power-temp-util/ucs-credentials.yml)
  - [telegraf/telegraf.d/ucs-power-temp-util/ucs-servers.yml](telegraf/telegraf.d/ucs-power-temp-util/ucs-servers.yml)
  - [telegraf/telegraf.d/ucs-power-temp-util/get-ucs-power-temp-util-idb.py](telegraf/telegraf.d/ucs-power-temp-util/get-ucs-power-temp-util-idb.py) lines #15-#16
- ACI APIC - see:
  - [telegraf/telegraf.d/apic/get-switch-power.py](telegraf/telegraf.d/apic/get-switch-power.py)
  - [telegraf/telegraf.d/telegraf-switch-apic.conf](telegraf/telegraf.d/telegraf-switch-apic.conf)
- Raritan PDUs - see:
  - [telegraf/telegraf.d/raritan-power/get-raritan.py](telegraf/telegraf.d/raritan-power/get-raritan.py)
  - [telegraf/telegraf.d/telegraf-raritan-pdu.conf](telegraf/telegraf.d/telegraf-raritan-pdu.conf)
- Eaton PDUs - see:
  - [telegraf/telegraf.d/telegraf-eaton-pdu.conf](telegraf/telegraf.d/telegraf-eaton-pdu.conf)
- Electricity Maps (CO2 Signal) - see:
  - [telegraf/telegraf.d/get-co2eqkwh.py](telegraf/telegraf.d/get-co2eqkwh.py)
  - [telegraf/telegraf.d/telegraf-electricitymap.conf](telegraf/telegraf.d/telegraf-electricitymap.conf)

1. Define the host IP (host where the containers are located), the proxy (if required), set credentials for InfluxDB, the proxy and, ideally, obtain a new CO2 Signal token from https://www.co2signal.com/.

    _Note_: InfluxDB token regeneration is needed when new credentials are used. To generate a new token, launch the InfluxDB service, access its UI at <HOST_IP>:8086 and follow these guidelines: https://docs.influxdata.com/influxdb/cloud/security/tokens/create-token.

    ```bash
    $ cd ../stack
    $ cp .env.example .env
    $ vi .env

    HTTPS_PROXY=

    HOST_IP=<enter IP address of host>

    DOCKER_INFLUXDB_INIT_MODE=setup
    # 1. Authentication to db
    DOCKER_INFLUXDB_INIT_USERNAME=<enter username>
    DOCKER_INFLUXDB_INIT_PASSWORD=<enter password>
    # 2. Resources or db
    DOCKER_INFLUXDB_INIT_ORG=cisco
    DOCKER_INFLUXDB_INIT_BUCKET=bucket1
    DOCKER_INFLUXDB_INIT_RETENTION=365d
    DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=<enter new influxdb token if the organisation and bucket are changed>

    CO2_SIGNAL_TOKEN=<enter token>
    ```

2. Configure data sources information.
   
   _Note_: Consider backing up the configuration files outside the  `telegraf.d` folder and keeping in this folder only the files relevant for your environment.

    ```bash
    cd telegraf/telegraf.d
    ```

   ### IOS-XR routers and NX-OS switches
   The collector listens on port 57500 for incoming gRPC telemetry.
   
   Map devices to locations for Electricity Maps:
   ```bash
   vi telegraf-mapping.conf

   # See sections of processors.enum
   ```
   ### Meraki switches
   The collector uses the Meraki Python SDK to retrieve the data from the Meraki Dashboard API.

   Configure API key and organization ID:
   ```bash
   vi meraki/get-meraki-power.py
   # Replace with your API key
    api_key = "sample-api-key"
    # Replace with your organization ID
    org_id = "sample-organization-id"
   ```

   ### ACI APIC nodes
   Credentials and list of APICs:
    ```bash
    vi apic/get-switch-power.py

    # Example: 
    apics = {"apic0.domain.com": ""}
    nodes = {"3331": {}, "3332": {}}
    username = 'user'
    password = 'fgklfgkfl'
    ```

   ### UCSs

   #### REDFISH API

   List of servers, system identifiers and credentials:
    ```bash
    vi telegraf-redfish.conf

    # Create one inputs.redfish entry for each server, e.g.:

    [[inputs.redfish]]
        address = "https://server-1.domain.com"
        computer_system_id = "XXXXXXXXXXX"
        username = "admin"
        password = "dfgkldfgkl"
        [...]
    ```

   Map servers to racks and locations for Electricity Maps:
    ```bash
    vi telegraf-mapping.conf

    # See sections of processors.enum
    ```

   #### CIMC API

   Credentials:
    ```bash
    vi ucs-power-temp-util/ucs-credentials.yml

    ucs:
        username: <username>
        password: <password>
    ```

   List of UCSs:
    ```bash
    vi ucs-power-temp-util/ucs-servers.yml

    # Example with format name: IP
    servers:
        # Rack X:
        server-1: 10.10.10.42
    ```

   Map servers to racks and locations for Electricity Maps:
    ```bash
    vi telegraf-mapping.conf

    # See sections of processors.enum
    ```

   #### UCSM API

   Credentials:
    ```bash
    vi ucs-power-temp-util/ucsm-credentials.yml

    ucs_domains:
        username: <username>
        password: <password>
    ```

   List of UCSs:
   ```bash
   vi ucs-power-temp-util/ucsm-domains.yml

    ucs_domains:
        # Rack X:
        LAB1: 10.10.10.42
   ```

   Map servers to racks and locations for Electricity Maps:
    ```bash
    vi telegraf-mapping.conf

    # See sections of processors.enum
    ```

   ### Raritan PDUs

   Credentials:
    ```bash
    vi raritan-power/raritan-credentials.yml

    pdu:
        username: <username>
        password: <password>
    ```

   List of PDUs:
    ```bash
    vi raritan-power/raritan-pdus.yml

    # Example with format name: IP
    pdus:
        pdu-1: 10.10.10.42
    ```

   ### Eaton PDUs
   List of PDUs:
    ```bash
    vi telegraf-eaton-pdu.conf

    # Edit line #4. Example:
    [[inputs.snmp]]
        agents = ["10.10.10.42"]
    ```

   ### CO<sub>2</sub>-eq emissions
   Customize countries for which to fetch the CO<sub>2</sub>-eq emissions data. See line #13 and subsequent lines in `get-co2eqkwh.py`
   ```bash
   countryCodes = ["DE", "ES", "FR", "IT-CNO", "IT-CSO", "IT-SO"]
   ```

### Telemetry streaming

To configure telemetry streaming, see [the configuration files located here](./mdt-config).

## Installation

### Create the stack of containers

Log out and log in or re-log in to allow the user to run the docker command:

```bash
sudo su - <user>
```

Bring up each service individually:
```bash
$ cd stack

$ docker-compose up -d influxdb
$ docker-compose up -d telegraf
$ docker-compose up -d grafana
```

Alternatively, bring up all services:
```bash
$ cd ../../installer

$ bash 04.create-stack.sh
```
