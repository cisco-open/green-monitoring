# FAQ

- [FAQ](#faq)
  - [Cleanup database](#cleanup-database)
  - [Support a non-local database instance](#support-a-non-local-database-instance)


## Cleanup database

For change of configurations or data removal:

```bash
docker stop influxdb; docker rm influxdb

rm -r stack/influxdb/influxdb-data-* 
git checkout stack/influxdb/influxdb-data-etc/.empty stack/influxdb/influxdb-data-var/lib/influxdb2/.empty

docker-compose up -d influxdb
```

## Support a non-local database instance

In order to use data from database instances that are different than the `influxdb` service, identified by UID _INFLUXDB2B082CADEA38E_, see this reference: https://github.com/grafana/grafana/discussions/45230#discussioncomment-4088203.

In short, it is required to either make a change of UIDs for the dashboard file in question or to move to a generic approach by not specifying the UID.

TBD.