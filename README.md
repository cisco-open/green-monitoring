# Green Monitoring Stack

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)


## Table of contents

- [Green Monitoring Stack](#green-monitoring-stack)
  - [Table of contents](#table-of-contents)
  - [About the project](#about-the-project)
    - [KPIs](#kpis)
    - [Technology stack](#technology-stack)
  - [Getting started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Configuration](#configuration)
    - [Installation](#installation)
  - [Usage](#usage)
    - [Access](#access)
    - [Dashboards](#dashboards)
  - [Specifications](#specifications)
  - [FAQ](#faq)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)
  - [Acknowledgements](#acknowledgements)


## About the project

A monitoring stack with samples for collection and data exploration for sustainability purposes.

The data is collected from Network, DC (compute / storage) infrastructure, third-party devices and external sources to be able to understand the **energy consumption** and its relation to traffic and bandwidth, the **cost** and the **carbon footprint** of the environment at various levels of granularity.

### KPIs

| Element | KPI |
| :---------- | :------------ |
| network device | power <br> power supply load <br> power supply efficiency <br> <br> traffic <br> bandwidth utilization <br> power consumption ratio (PCR) - [reference](SPECS.md#power-consumption-ratio-pcr) <br> <br> CO<sub>2</sub>-eq emissions (+ historical) <br> cost|
| server | power <br> utilization <br> temperature <br> <br> CO<sub>2</sub>-eq emissions <br> cost |
| pdu | power |
| rack | power <br> _TBD:_ temperature|

### Technology stack

*Architecture*
![Architecture](stack/doc/img/architecture.png)

Captures data from:
- IOS-XR routers
- NX-OS switches
- Meraki switches
- UCS servers
- ACI APIC
- Raritan PDUs
- Eaton PDUs

Stores data in:
- InfluxDB v2

Exposes data in:
- Grafana

Data Flow:

    IOS-XR
    NX-OS
    Meraki
    ACI APIC                   -> Telegraf     ->     InfluxDB     -> Grafana
    UCS: REDFISH/CIMC/UCSM
    Raritan PDUs
    Eaton PDUs

---

## Getting started

### Prerequisites

[Use these instructions](./stack/README.md#prerequisites).

### Configuration
[Use these instructions](./stack/README.md#configuration).

### Installation
[Use these instructions](./stack/README.md#installation).

## Usage

### Access

Access the two following WebUIs by replacing the `HOST_IP` placeholder with the reachable IP address of the host that runs the stack:

- [Grafana](http://HOST_IP:3000) - hosts custom visualizations.
- [Influx](http://HOST_IP:8086) (_credentials based on [.env](./stack/.env)_) - for exploration of raw data.

### Dashboards

Overview power - Meraki - organization/switches
![Overview power - Meraki - organization/switches](stack/doc/img/overview%20power,%20carbon%20emissions/meraki.png)

Overview power - DC - Nexus
![Overview power - DC - Nexus](stack/doc/img/overview%20power%2C%20carbon%20emissions/nexus.png)

Overview CO<sub>2</sub>-eq emissions - DC - Nexus
![Overview CO2-eq emissions - DC - Nexus](stack/doc/img/overview%20power,%20carbon%20emissions/nexus%20-%20co2eq%20emissions.png)

Overview power - NCS, ASR 9K, Cisco 8K
![Overview power - NCS, ASR 9K, Cisco 8K](stack/doc/img/overview%20power%2C%20carbon%20emissions/ncs%2C%20asr%209k%2C%208k.png)

Overview CO<sub>2</sub>-eq emissions - NCS, ASR 9K, Cisco 8K
![Overview CO2-eq emissions - NCS, ASR 9K, Cisco 8K](stack/doc/img/overview%20power,%20carbon%20emissions/ncs,%20asr%209k,%208k%20-%20co2eq%20emissions.png)

Historical overview of CO<sub>2</sub>-eq emissions - Fretta
![Historical overview of CO2-eq emissions - Fretta](stack/doc/img/carbon%20emissions/carbon%20emissions%20-%20fretta.png)

Power - DC - UCS
![Power - DC - UCS](stack/doc/img/ucs/ucs%20-%20power.png)

Temperature - DC - UCS
![Temperature - DC - UCS](stack/doc/img/ucs/ucs%20-%20temperature.png)

Utilization - DC - UCS
![Utilization - DC - UCS](stack/doc/img/ucs/ucs%20-%20utilization.png)

Rack view - DC - UCS 1/3
![Rack view - DC - UCS 1/3](stack/doc/img/ucs/ucs%20-%20rack%20view%201.png)

Rack view - DC - UCS 2/3
![Rack view - DC - UCS 2/3](stack/doc/img/ucs/ucs%20-%20rack%20view%202.png)

Rack view - DC - UCS 3/3
![Rack view - DC - UCS 3/3](stack/doc/img/ucs/ucs%20-%20rack%20view%203.png)

PDUs - Raritan
![PDUs - Raritan](stack/doc/img/pdus/raritan%20pdus.png)

PDUs - Eaton
![PDUs - Eaton](stack/doc/img/pdus/eaton%20pdus.png)

Cost - DC - Nexus and UCS
![Cost - DC - Nexus and UCS](stack/doc/img/cost/cost-nexus-ucs.png)

PCR (Power consumption ratio) versus Traffic
![PCR versus traffic - Cisco 8201](stack/doc/img/pcr/pcr-vs-traffic-cisco-8k.png)

PCR (Power consumption ratio) versus Bandwidth utilization - concept
![PCR versus bandwidth utilization](stack/doc/img/pcr/pcr-vs-bw-utilization-concept.png)

PCR (Power consumption ratio) versus Bandwidth utilization - NCS
![PCR versus bandwidth utilization](stack/doc/img/pcr/pcr-vs-bw-utilization-ncs.png)

PCR (Power consumption ratio) versus Bandwidth utilization - ASR 9K and Cisco 8K
![PCR versus bandwidth utilization](stack/doc/img/pcr/pcr-vs-bw-utilization-asr-9k-cisco-8k.png)

Bandwidth utilization and distribution per interface
![PCR versus bandwidth utilization](stack/doc/img/pcr/bw-utilization-and-distribution-per-if.png)

## Specifications

The collections available are documented in [SPECS.md](SPECS.md).

## FAQ

See [FAQ.md](FAQ.md).

## Contributing

Contributions are highly appreciated. Please follow the guidelines documented in [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

Distributed under the **Apache License Version 2.0**. See the [LICENSE](./LICENSE) for more information.

## Contact

Cristina Precup - cprecup@cisco.com

## Acknowledgements

- [Cisco](https://www.cisco.com)
- [CO2 Signal](https://www.co2signal.com)
- [Electricity Maps](https://www.electricitymaps.com)
- [Influx Data](https://www.influxdata.com)
- [Grafana Labs](https://grafana.com)
- [Eaton](https://www.eaton.com)
- [Raritan](https://www.raritan.com)
