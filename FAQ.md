# FAQ

- [FAQ](#faq)
  - [Cleanup database](#cleanup-database)
  - [Set database credentials](#set-database-credentials)
  - [Support a non-local database instance](#support-a-non-local-database-instance)


## Cleanup database

For change of configurations or data removal:

```bash
docker stop influxdb; docker rm influxdb

rm -r stack/influxdb/influxdb-data-* 
git checkout stack/influxdb/influxdb-data-etc/.empty stack/influxdb/influxdb-data-var/lib/influxdb2/.empty

docker-compose up -d influxdb
```

## Set database credentials
When creating a `.env` file as per the `.env.example`, it is recommended to change the credentials for the database (`DOCKER_INFLUXDB_INIT_USERNAME` and `DOCKER_INFLUXDB_INIT_PASSWORD`). Consequently, InfluxDB token _regeneration_ may be needed when new credentials are used. Alternatively, change the credentials from Influx's CLI by following these instructions: https://docs.influxdata.com/influxdb/v2/admin/users/change-password.

To generate a new token for InfluxDB, launch the InfluxDB service and access its UI at <HOST_IP>:8086. Follow these guidelines to generate a new token: https://docs.influxdata.com/influxdb/cloud/security/tokens/create-token and save this token in `.env` as `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN`.

Once ready, launch the Telegraf and Grafana services that will use the token to perform read/write operations on the database.

## Support a non-local database instance

In order to use data from database instances that are different than the `influxdb` service, identified by UID _INFLUXDB2B082CADEA38E_, see this reference: https://github.com/grafana/grafana/discussions/45230#discussioncomment-4088203.

In short, it is required to either make a change of UIDs for the dashboard file in question or to move to a generic approach by not specifying the UID.

TBD.