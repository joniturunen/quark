# Quark the Discord bot

> Bot monitors channel member.activities and forms a time series entries to InfluxDB (docker)

You need to create `.env` file that holds your token string etc for the Discord connection. Check the example from below.

### Todo

- need to switch to hours or make up a logic to show minutes when under treshold otherwise use hours
- need a logic to handle several servers and generate stats from them
- need a way to check if `!bar <member>` exists, if not set proper message content
- put Quark in a container

## Commands

You can check the commands from [quark.py](quark.py).

- ping
- p2 (int)
- rule (int)

## Rules of Acquistion

Source: [Gist](https://gist.githubusercontent.com/darkyen/120c46739985ebf3b39b/raw/5ef59ed209f580bf0a7885945e816445aea178e3/gistfile1.txt)

## InfluxDB initialization

You can use `docker-compose up` to run a local influxdb instance.
In order for the connection to work you need to create a user login and database via influx cli.

```bash
$docker exec -it influxdb_container bash

$influx
> CREATE DATABASE quarksbar
> CREATE USER quarkdb WITH PASSWORD '(p)assw0rd$'
```

Note the password you create needs to be in `.env`.

## Environment variables

Bot uses settings.py and a **qenv** class object to pass around the parameters. Create `.env` file in order to use the bot. Here is a example.

```txt
DISCORD_TOKEN=<token for the bot to connect>
DISCORD_SERVER=<server to monitor>
ACTIVITY_FILTERS=Spotify|Visual Studio|!donate
BOT_DESC="I'm not just some venal Ferengi trying to take their money. I'm Quark, slayer of Klingons!"
BOT_OWNER_ID=<your discord id>
BOT_OWNER_NAME=<your discord name>
BOT_ID=<your own bot id>
GOOGLE_API_KEY=<this is needed for !yt commands>
INFLUXDB_HOST=localhost
INFLUXDB_NAME=quarksbar
INFLUXDB_PORT=8086
INFLUXDB_USER=quarkdb
INFLUXDB_PASS=(p)assw0rd$
MONITORING_INTERVAL_IN_SECONDS=5'
MONITORING_FILTER_SERVERS="das|test"
BAR_COLORS="#9CC3CE|#BCC4BE|#C59D8B"
```

`ACTIVITY_FILTERS` is a | -separated list of things you would not want to monitor as game activity.

## Running on Raspberry Pi (raspbian)

You need few installations for things to work. Mostly stuff for barcharts to work. Oh yeah, and you need Docker with docker-compose aswell to run influxdb etc.

```bash
sudo apt-get install libopenjp2-7
sudo apt-get install libatlas-base-dev
sudo apt install libtiff5
```

## Backup influxdb data

For running 1.8.x version of influxdb


Run inside the container:

```bash
influxd backup -portable .
```

Then from outside the container:

```bash
docker cp influxdb_container:/opt/quark_db_backup /somepath/onyour/localmachine
```
