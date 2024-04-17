# Specifications
- [Specifications](#specifications)
  - [Collections](#collections)
  - [Paths, class IDs, SNMP MIBs and YANG models](#paths-class-ids-snmp-mibs-and-yang-models)
    - [Meraki](#meraki)
    - [REDFISH](#redfish)
      - [UCS](#ucs)
    - [CIMC: Class IDs](#cimc-class-ids)
      - [UCS](#ucs-1)
    - [UCSM](#ucsm)
    - [SNMP](#snmp)
    - [TELEMETRY](#telemetry)
      - [Nexus 3K, Nexus 9K](#nexus-3k-nexus-9k)
        - [C9372PX: NX-OS 9.3(7)](#c9372px-nx-os-937)
      - [NCS](#ncs)
        - [NCS-540: IOS-XR 7.4.1](#ncs-540-ios-xr-741)
        - [NCS-540L: IOS-XR 7.7.1 LNT](#ncs-540l-ios-xr-771-lnt)
        - [NCS-55A2: IOS-XR 7.3.2](#ncs-55a2-ios-xr-732)
        - [NCS-5504: IOS-XR 7.2.2](#ncs-5504-ios-xr-722)
        - [NCS-5508: IOS-XR 7.3.2](#ncs-5508-ios-xr-732)
      - [ASR-9K](#asr-9k)
        - [ASR-9001: IOS-XR 7.3.1](#asr-9001-ios-xr-731)
        - [ASR-9904: IOS-XR 7.3.2](#asr-9904-ios-xr-732)
        - [ASR-9903: IOS-XR 7.3.2](#asr-9903-ios-xr-732)
      - [Cisco 8201](#cisco-8201)
        - [IOS-XR 7.3.2 LNT](#ios-xr-732-lnt)
        - [IOS-XR 7.7.1 LNT](#ios-xr-771-lnt)
        - [IOS-XR 7.10.1 LNT](#ios-xr-7101-lnt)
  - [Power consumption ratio (PCR)](#power-consumption-ratio-pcr)

## Collections

| Data source | Configuration | Measurement(s) | Collection scripts | Frequency | Data enrichment script (tags) | Dashboard(s) |
| :---------- | :------------ | :------------- | :----------------- | :-------- | :------------- | :----------- |
| NCS | [ncs-540.cfg](stack/mdt-config/ncs-540.cfg)<br> [ncs-50xx.cfg](stack/mdt-config/ncs-50xx.cfg)<br> [ncs-540L.cfg](stack/mdt-config/ncs-540L.cfg)<br> [ncs-560-er.cfg](stack/mdt-config/ncs-560-er.cfg) | Cisco-IOS-XR-sysadmin-fretta-envmon-ui:environment/oper/power/location/pem_attributes<br>  <br> Cisco-IOS-XR-envmon-oper:environmental-monitoring/rack/nodes/node/sensor-types/sensor-type/sensor-names/sensor-name <br> Cisco-IOS-XR-envmon-oper:power-management/rack/chassis <br> Cisco-IOS-XR-envmon-oper:power-management/rack/consumers/consumer-nodes/consumer-node <br> Cisco-IOS-XR-envmon-oper:power-management/rack/producers/producer-nodes/producer-node <br> <br>  Cisco-IOS-XR-sysadmin-uea-envmon-ui:environment/oper/power/location/pem_attributes <br> <br> \_Others:*<br> Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/total/data-rate _(bandwidth, traffic)_ <br> Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief _(interface states)_ | [telegraf-xr-and-nxos.conf](stack/telegraf/telegraf.d/telegraf-xr-and-nxos.conf) | 30-60-120s | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) | Power <br> Carbon emissions <br> Cost <br> Carbon emissions - historical - Fretta <br> Bandwidth Utilization |
| ASR 9K | [asr-9903.cfg](stack/mdt-config/asr-9903.cfg) <br> [asr-9904.cfg](stack/mdt-config/asr-9904.cfg) | _Power:_ <br> Cisco-IOS-XR-sysadmin-asr9k-envmon-ui:environment/oper/power/location/pem*attributes <br> <br> \_Others:* <br> Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/total/data-rate _(bandwidth, traffic)_ <br> Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief _(interface states)_ | [telegraf-xr-and-nxos.conf](stack/telegraf/telegraf.d/telegraf-xr-and-nxos.conf) | 30s | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) | Power <br> Carbon emissions <br> Cost <br> Bandwidth Utilization |
| Cisco 8K | [cisco-router-8201.cfg](stack/mdt-config/cisco-router-8201.cfg) | Cisco-IOS-XR-envmon-oper:environmental-monitoring/rack/nodes/node/sensor-types/sensor-type/sensor-names/sensor-name <br> Cisco-IOS-XR-envmon-oper:power-management/rack/chassis <br> Cisco-IOS-XR-envmon-oper:power-management/rack/consumers/consumer-nodes/consumer-node <br> Cisco-IOS-XR-envmon-oper:power-management/rack/producers/producer-nodes/producer-node <br> Cisco-IOS-XR-invmgr-oper:inventory/entities/entity/attributes/env-sensor-info <br> Cisco-IOS-XR-invmgr-oper:inventory/entities/entity/attributes/inv-basic-bag <br> <br> _Others:_<br> Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/total/data-rate _(bandwidth, traffic)_ <br> Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief _(interface states)_ | [telegraf-xr-and-nxos.conf](stack/telegraf/telegraf.d/telegraf-xr-and-nxos.conf) | 30s | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) | Power <br> Carbon emissions <br> Cost <br> PCR versus Traffic <br> Bandwidth Utilization |
| Meraki | | meraki-switch | [stack/telegraf/telegraf.d/meraki/get-meraki-power.py](stack/telegraf/telegraf.d/meraki/get-meraki-power.py) <br> [stack/telegraf/telegraf.d/telegraf-switch-meraki.conf](stack/telegraf/telegraf.d/telegraf-switch-meraki.conf) | 1h | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) | Meraki |
| Nexus | [nexus9k-c9372px.cfg](stack/mdt-config/nexus9k-c9372px.cfg) | show environment power | [telegraf-xr-and-nxos.conf](stack/telegraf/telegraf.d/telegraf-xr-and-nxos.conf) | 30s | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) | Power <br> Carbon emissions <br> Cost <br> Cost - Nexus and UCS |
| ACI APIC |  | apic-switch | [get-switch-power.py](stack/telegraf/telegraf.d/apic/get-switch-power.py) <br> [telegraf-switch-apic.conf](stack/telegraf/telegraf.d/telegraf-switch-apic.conf) | 3m | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) | Power <br> Carbon emissions <br> Cost |
| UCS REDFISH |  | redfish_power_powersupplies <br> redfish_thermal_temperatures | [telegraf-redfish.conf](stack/telegraf/telegraf.d/telegraf-redfish.conf) | 60m | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) | Cost - UCS and Nexus |
| UCS CIMC |  | cimc-ucs-power <br> cimc-ucs-temperature <br> cimc-ucs-utilization | [get-ucs-power-temp-util-idb.py](stack/telegraf/telegraf.d/ucs-power-temp-util/get-ucs-power-temp-util-idb.py) <br> [telegraf-ucs-cimc.conf](stack/telegraf/telegraf.d/telegraf-ucs-cimc.conf) | 60m | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) | UCS <br> UCS - Rack view |
| UCSM |  | ucsm-chassis-power <br> ucsm-server-power <br> ucsm-fabric-interconnect-power | [get-ucsm-power-temp-util-idb.py](stack/telegraf/telegraf.d/ucs-power-temp-util/get-ucsm-power-temp-util-idb.py) <br> [telegraf-ucsm.conf](stack/telegraf/telegraf.d/telegraf-ucsm.conf) | 60m | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) |  |
| Raritan PDUs |  | raritan-pdu | [get-raritan.py](stack/telegraf/telegraf.d/raritan-power/get-raritan.py) <br> [telegraf-raritan-pdu.conf](stack/telegraf/telegraf.d/telegraf-raritan-pdu.conf) | 1m | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) | Raritan PDUs |
| Eaton PDUs |  | eaton_input_power <br> eaton_output_power | [telegraf-eaton-pdu.conf](stack/telegraf/telegraf.d/telegraf-eaton-pdu.conf) | 60s | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) | Eaton PDUs |
| Electricity Maps - CO2 emissions/kWh |  | electricity-map | [get-co2eqkwh.py](stack/telegraf/telegraf.d/get-co2eqkwh.py) <br> [telegraf-electricitymap.conf](stack/telegraf/telegraf.d/telegraf-electricitymap.conf) | 15m | [telegraf-mapping.conf](stack/telegraf/telegraf.d/telegraf-mapping.conf) | Carbon emissions <br> Carbon emissions - historical - Fretta |

## Paths, class IDs, SNMP MIBs and YANG models

The resources considered for power and temperature information are documented below.

_Note_: For sample device configuration of the IOS-XR, NX-OS devices, refer to [the configuration files located here](stack/mdt-config).

_Note_: The elements highlighted in **bold** are those that have been used for the visualizations.

### Meraki

| Element | Operation ID |
| :------------------ | :------------------ |
| organization    | [getOrganizationSummaryTopSwitchesByEnergyUsage](https://developer.cisco.com/meraki/api-v1/get-organization-summary-top-switches-by-energy-usage) |
| switch/port    | [getDeviceSwitchPortsStatuses](https://developer.cisco.com/meraki/api-v1/get-device-switch-ports-statuses) |

### REDFISH
#### UCS

| Redfish property path            |
| :------------------ |
| **redfish_power_powersupplies**    |
| **redfish_thermal_temperatures**    |

### CIMC: Class IDs

References:
- [CIMC Python SDK source code](https://github.com/CiscoUcs/imcsdk)
- [CIMC MIM](https://imcsdk.readthedocs.io/en/latest/imcsdk_ug.html#management-information-model)
- [Class IDs](https://ciscoucs.github.io/imcsdk_docs/imcsdk.html?highlight=query_dn#imcsdk.imcconstants.NamingId)

#### UCS

| Class ID            | Python constant                 |
| :------------------ | :------------------------------ |
| **powerMonitor**    | **NamingId.POWER_MONITOR**      |
| **equipmentPsu**    | **NamingId.EQUIPMENT_PSU**      |
| powerBudget         | NamingId.POWER_BUDGET           |
| consumedPower       | NamingId.CONSUMED_POWER         |
| cpuPowerLimit       | NamingId.CPU_POWER_LIMIT        |
| maxCpuPower         | NamingId.MAX_CPU_POWER          |
| minCpuPower         | NamingId.MIN_CPU_POWER          |
| maxMemoryPower      | NamingId.MAX_MEMORY_POWER       |
| maxPower            | NamingId.MAX_POWER              |
| minPower            | NamingId.MIN_POWER              |
| memoryPowerLimit    | NamingId.MEMORY_POWER_LIMIT     |
| computeMbPowerStats | NamingId.COMPUTE_MB_POWER_STATS |
| power               | NamingId.POWER                  |
| powerLimit          | NamingId.POWER_LIMIT            |
| powerState          | NamingId.POWER_STATE            |

### UCSM

| UCSM property path            |
| :------------------ |
| **EquipmentChassisStats**    |
| **ComputeMbPowerStats**    |
| **EquipmentPsuInputStats**    |

### SNMP

References:
 - [Cisco MIBs](https://github.com/cisco/cisco-mibs/tree/main/v2)
 - [Eaton MIBs](http://powerquality.eaton.com/Support/Software-Drivers/Downloads/ePDU/EATON-EPDU-MIB.zip)

### TELEMETRY

Reference:
- [YANG models for IOS-XR, IOS-XE, NX-OS platforms](https://github.com/YangModels/yang/tree/master/vendor/cisco)

#### Nexus 3K, Nexus 9K

##### C9372PX: NX-OS 9.3(7)
| NX-API command         | Fields                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **show** env **power** | psmodel<br> actual_out<br> actual_input<br> tot_capa<br> ps_status<br> powersup/voltage_level=12i<br> powersup/power_summary/ps_redun_mode<br> powersup/power_summary/ps_oper_mode<br> powersup/power_summary/tot_pow_capacity<br> powersup/power_summary/tot_gridA_capacity<br> powersup/power_summary/tot_gridB_capacity<br> powersup/power_summary/cumulative_power<br> **powersup/power_summary/tot_pow_out_actual_draw<br>** **powersup/power_summary/tot_pow_input_actual_draw<br>** powersup/power_summary/tot_pow_alloc_budgeted<br> powersup/power_summary/available_pow<br> powersup/TABLE_psinfo |

#### NCS


##### NCS-540: IOS-XR 7.4.1
| Model                                           | Telemetry Path(s)                                                                                                                                                                                                                                                                                                                                     |
| :---------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cisco-IOS-XR-sysadmin-fretta-envmon-ui.yang** | **Cisco-IOS-XR-sysadmin-fretta-envmon-ui:environment/oper/power** <br> Specifically in Grafana: <br> - **[...]/location/pem_attributes/system_power_input** <br> - **[...]/location/pem_attributes/power_resrv_and_alloc**                                                                                                                            |
| Cisco-IOS-XR-invmgr-oper.yang                   | <br>- Cisco-IOS-XR-invmgr-oper:inventory/racks/rack/powershelf  <br>- Cisco-IOS-XR-invmgr-oper:inventory/entities/entity/attributes/inv-basic-bag/allocated-power <br>- [...]                                                                                                                                                                         |
| Cisco-IOS-XR-plat-chas-invmgr-ng-oper.yang      | Cisco-IOS-XR-plat-chas-invmgr-ng-oper:platform-inventory/racks/rack/attributes/fru-info/module-power-administrative-state (only state)                                                                                                                                                                                                                |
| Cisco-IOS-XR-sdr-invmgr-diag-oper.yang          | <br>- Cisco-IOS-XR-sdr-invmgr-diag-oper:diag/racks/rack/fan-trays/fan-tray/fanses/fans/information/power-consumption <br>- Cisco-IOS-XR-sdr-invmgr-diag-oper:diag/racks/rack/power-shelfs/power-shelf/power-shelf-name <br>- Cisco-IOS-XR-sdr-invmgr-diag-oper:diag/racks/rack/power-shelfs/power-shelf/power-supplies/power-supply/power-supply-name |
| openconfig-platform.yang                        | openconfig-platform:components/component/state                                                                                                                                                                                                                                                                                                        |
| Cisco-IOS-XR-sysadmin-show-inv.yang             | Cisco-IOS-XR-sysadmin-show-inv:inventory/power (power supplies)                                                                                                                                                                                                                                                                                       |
| _Others_: <br><br> **Cisco-IOS-XR-infra-statsd-oper.yang** <br> <br> **Cisco-IOS-XR-pfi-im-cmd-oper.yang**      | **Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/total/data-rate/[input/output]-data-rate** <br> <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/type** <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/state**  <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/bandwidth**                      |

##### NCS-540L: IOS-XR 7.7.1 LNT

| Model                             | Telemetry Path(s)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Observations |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- |
| **Cisco-IOS-XR-envmon-oper.yang** | <br>- Cisco-IOS-XR-envmon-oper:environmental-monitoring <br>- **Cisco-IOS-XR-envmon-oper:environmental-monitoring/rack/nodes/node/sensor-types/sensor-type/sensor-names/sensor-name** <br>- **Cisco-IOS-XR-envmon-oper:environmental-monitoring/rack/nodes/node/sensor-types/sensor-type/type** <br>- **Cisco-IOS-XR-envmon-oper:environmental-monitoring/rack/nodes/node/sensor-types/sensor-type/type=power** <br>- Cisco-IOS-XR-envmon-oper:power-management <br> <br>- **Cisco-IOS-XR-envmon-oper:power-management/rack/producers** <br> Specifically, in Grafana: <br> - **[...]/producer-node/pem_info_array/current_in_a** <br> - **[...]/producer-node/pem_info_array/current_in_b** <br> - **[...]/producer-node/pem_info_array/voltage_in_a** <br> - **[...]/producer-node/pem_info_array/voltage_in_b** <br>- **[...]/producer-node/pem_info_array/voltage_out** <br>- **[...]/producer-node/pem_info_array/current_out** <br><br>- **Cisco-IOS-XR-envmon-oper:power-management/rack/consumers/consumer-nodes** <br><br>- **Cisco-IOS-XR-envmon-oper:power-management/rack/chassis** |
|                                   |
| _Others_: <br><br> **Cisco-IOS-XR-infra-statsd-oper.yang** <br> <br> **Cisco-IOS-XR-pfi-im-cmd-oper.yang** | **Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/total/data-rate/[input/output]-data-rate** <br> <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/type** <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/state** <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/bandwidth**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

##### NCS-55A2: IOS-XR 7.3.2
| Model                                           | Telemetry Path(s)                                                                                                                                            |
| :---------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cisco-IOS-XR-sysadmin-fretta-envmon-ui.yang** | **Cisco-IOS-XR-sysadmin-fretta-envmon-ui:environment/oper/power** <br> Specifically, in Grafana: <br> - **[...]/location/pem_attributes/system_power_input** |

_Additionally, see table above, section **Others**_.

##### NCS-5504: IOS-XR 7.2.2

_See table below._

##### NCS-5508: IOS-XR 7.3.2
| Model                                           | Telemetry Path(s)                                                                                                                                              |
| :---------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cisco-IOS-XR-sysadmin-fretta-envmon-ui.yang** | **Cisco-IOS-XR-sysadmin-fretta-envmon-ui:environment/oper/power** <br> Specifically, in Grafana: <br> - **[...]/location/pem_attributes/power_consumed/value** |

_Additionally, see table above, section **Others**_.

#### ASR-9K

##### ASR-9001: IOS-XR 7.3.1


| Model                                      | Telemetry Path(s)                                                                                                                                                                                                                                                                                                                                                                                               | Observations |
| :----------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- |
| Cisco-IOS-XR-sysadmin-asr9k-envmon-ui.yang | - Cisco-IOS-XR-sysadmin-asr9k-envmon-ui:environment/oper/power/location<br>- [...]/pem_attributes/input_power_to_ps<br>- [...]/pem_attributes/output_power_from_ps<br>- [...]/pem_attributes/power_resrv_and_alloc<br>- [...]/pem_attributes/protection_power_capacity<br>- [...]/pem_attributes/system_power_input<br>- [...]/pem_attributes/system_power_used<br>- [...]/pem_attributes/usable_power_capacity |
|                                            |
|                                            | - Cisco-IOS-XR-sysadmin-asr9k-envmon-ui:environment/all/location<br>- [...]/power/pem_attributes/power_allocated<br>- [...]/power/pem_attributes/power_consumed<br>- [...]/power/pem_attributes/power_level<br>- [...]/power/pem_attributes/power_status                                                                                                                                                        |
|                                            |
|                                            | - Cisco-IOS-XR-sysadmin-asr9k-envmon-ui:power-mgmt/config (_no data here_)                                                                                                                                                                                                                                                                                                                                      |
| Cisco-IOS-XR-sdr-invmgr-diag-oper.yang     | - Cisco-IOS-XR-sdr-invmgr-diag-oper:diag/racks/rack/power-shelfs/power-shelf/power-supplies/power-supply<br>- Cisco-IOS-XR-sdr-invmgr-diag-oper:diag/racks/rack/slots (power-consumption per card instances of slot)                                                                                                                                                                                            |
| Cisco-IOS-XR-drivers-media-eth-oper.yang   | - Cisco-IOS-XR-drivers-media-eth-oper:ethernet-interface/interfaces/interface/phy-info/phy-details/transceiver-tx-power<br>- Cisco-IOS-XR-drivers-media-eth-oper:ethernet-interface/interfaces/interface/phy-info/phy-details/transceiver-rx-power                                                                                                                                                              | _Optics_     |
| openconfig-platform.yang                   | - openconfig-platform:components/component/linecard/power-admin-state (not a measurement)<br>- openconfig-platform:components/component/power-supply<br>- openconfig-platform:components/component/state/allocated-power<br>- openconfig-platform:components/component/state/used-power                                                                                                                         |
|                                            |
|                                            | - openconfig-platform:components/component/transceiver/physical-channels/channel/state/input-power<br>- openconfig-platform:components/component/transceiver/physical-channels/channel/state/output-power<br>- openconfig-platform:components/component/transceiver/state/input-power<br>- openconfig-platform:components/component/transceiver/state/output-power                                              | _Optical_    |
| _Others_: <br><br> **Cisco-IOS-XR-infra-statsd-oper.yang** <br> <br> **Cisco-IOS-XR-pfi-im-cmd-oper.yang** | **Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/total/data-rate/[input/output]-data-rate** <br> <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/type** <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/state** <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/bandwidth** |

##### ASR-9904: IOS-XR 7.3.2
##### ASR-9903: IOS-XR 7.3.2


| Model                                          | Telemetry Path(s)                                                                                                                                                                                                                                                                                                                                                                                                              | Observations |
| :--------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- |
| **Cisco-IOS-XR-sysadmin-asr9k-envmon-ui.yang** | - **Cisco-IOS-XR-sysadmin-asr9k-envmon-ui:environment/oper/power/location** <br>- [...]/pem_attributes/input_power_to_ps<br>- [...]/pem_attributes/output_power_from_ps<br>- **[...]/pem_attributes/power_resrv_and_alloc** <br>- [...]/pem_attributes/protection_power_capacity<br>- **[...]/pem_attributes/system_power_input** <br>- [...]/pem_attributes/system_power_used<br>- [...]/pem_attributes/usable_power_capacity |
|                                                |
|                                                | - Cisco-IOS-XR-sysadmin-asr9k-envmon-ui:environment/all/location<br>- [...]/power/pem_attributes/power_allocated<br>- [...]/power/pem_attributes/power_consumed<br>- [...]/power/pem_attributes/power_level<br>- [...]/power/pem_attributes/power_status                                                                                                                                                                       |


#### Cisco 8201

##### IOS-XR 7.3.2 LNT

| Model                                    | Telemetry Path(s)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Observations |
| :--------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- |
| Cisco-IOS-XR-pwrmgmt-cfg.yang            | Cisco-IOS-XR-pwrmgmt-cfg:power-management                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Cisco-IOS-XR-envmon-cfg.yang             | Cisco-IOS-XR-envmon-cfg:environmental-monitoring                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **Cisco-IOS-XR-envmon-oper.yang**        | <br>- Cisco-IOS-XR-envmon-oper:environmental-monitoring <br>- **Cisco-IOS-XR-envmon-oper:environmental-monitoring/rack/nodes/node/sensor-types/sensor-type/sensor-names/sensor-name** <br>- **Cisco-IOS-XR-envmon-oper:environmental-monitoring/rack/nodes/node/sensor-types/sensor-type/type** <br>- **Cisco-IOS-XR-envmon-oper:environmental-monitoring/rack/nodes/node/sensor-types/sensor-type/type=power** <br>- Cisco-IOS-XR-envmon-oper:power-management <br> <br>- **Cisco-IOS-XR-envmon-oper:power-management/rack/producers** <br> Specifically, in Grafana: <br> - **[...]/producer-node/pem_info_array/current_in_a** <br> - **[...]/producer-node/pem_info_array/current_in_b** <br> - **[...]/producer-node/pem_info_array/voltage_in_a** <br> - **[...]/producer-node/pem_info_array/voltage_in_b** <br>- **[...]/producer-node/pem_info_array/voltage_out** <br>- **[...]/producer-node/pem_info_array/current_out** <br><br>- **Cisco-IOS-XR-envmon-oper:power-management/rack/consumers/consumer-nodes** <br><br>- **Cisco-IOS-XR-envmon-oper:power-management/rack/chassis** |
| Cisco-IOS-XR-invmgr-oper.yang            | - Cisco-IOS-XR-invmgr-oper:inventory/entities/entity/attributes/inv-basic-bag/allocated-power<br>- Cisco-IOS-XR-invmgr-oper:inventory/entities/entity/attributes/inv-basic-bag/power-capacity<br>- Cisco-IOS-XR-invmgr-oper:inventory/entities/entity/attributes/fru-info/power-administrative-state<br>- Cisco-IOS-XR-invmgr-oper:inventory/entities/entity/attributes/fru-info/power-current-measurement<br>- Cisco-IOS-XR-invmgr-oper:inventory/entities/entity/attributes/fru-info/power-administrative-state<br>- Cisco-IOS-XR-invmgr-oper:inventory/entities/entity/attributes/inv-eeprom-info/eeprom/power-consumption<br>- Cisco-IOS-XR-invmgr-oper:inventory/entities/entity/attributes/env-sensor-info[="Name of a power sensor?", e.g. 0/RP0/CPU0-MB_1_125V_IIN]<br>- Cisco-IOS-XR-invmgr-oper:inventory/racks/rack                                                                                                                                                                                                                                                                  |
| Cisco-IOS-XR-invmgr-diag-oper.yang       | Cisco-IOS-XR-invmgr-diag-oper:diag/racks/rack/power-shelfs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Cisco-IOS-XR-plat-chas-invmgr-ng-oper    | ? cannot be resolved - has information only on "is-powered" state ?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Cisco-IOS-XR-controller-optics-oper.yang | Cisco-IOS-XR-controller-optics-oper:optics-oper/optics-ports/optics-port/optics-info/voltage                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | _Optics_     |
|                                          |
| openconfig-platform.yang                 | - openconfig-platform:components/component/linecard/power-admin-state (not a measurement)<br>- openconfig-platform:components/component/power-supply<br>- openconfig-platform:components/component/state/allocated-power<br>- openconfig-platform:components/component/state/used-power                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| _Others_: <br><br> **Cisco-IOS-XR-infra-statsd-oper.yang** <br> <br> **Cisco-IOS-XR-pfi-im-cmd-oper.yang** <br> <br> **Cisco-IOS-XR-invmgr-oper.yang** | **Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/total/data-rate/[input/output]-data-rate** <br> <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/type** <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/state** <br> **Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/interface-briefs/interface-brief/bandwidth** <br> <br> **Cisco-IOS-XR-invmgr-oper:inventory/entities/entity/attributes/inv-basic-bag**            |

##### IOS-XR 7.7.1 LNT

_Same metrics as above_.

`Cisco-IOS-XR-envmon-oper:power-management/rack/producers/producer-node/pem_info_array/current_*|voltage_*` changed data type: `string` -> `integer`.

##### IOS-XR 7.10.1 LNT

_Same metrics as above_.

Additional fields introduced:

| Model                                    | Telemetry Path(s)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Observations |
| :--------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- |
| **Cisco-IOS-XR-envmon-oper.yang**        | Cisco-IOS-XR-envmon-oper:power-management/rack/producers <br> - [...]/producer-node/pem_info_array/mcurrent_in_a <br> - [...]/producer-node/pem_info_array/mcurrent_in_b <br> - [...]/producer-node/pem_info_array/mvoltage_in_a** <br> - [...]/producer-node/pem_info_array/mvoltage_in_b <br>- [...]/producer-node/pem_info_array/mvoltage_out <br>- [...]/producer-node/pem_info_array/mcurrent_out <br>                                                 | _Units of measurement in mA \| mV. The initial fields `current_in_a`, `current_in_b`, `voltage_in_a`, `voltage_in_b`, `current_out`, `voltage_out` are now in A \| V._     |

## Power consumption ratio (PCR)

This measurement shows the ratio between the rate of power and the rate of data per second, or, inversely, between the rate of data and the rate of power.

$`PCR = \frac{input\_power\_used}{[input | output\_]data\_rate} [\frac{W}{Gbps}]`$

Answers the question: _How much power is used for 1 Gbps data rate?_
