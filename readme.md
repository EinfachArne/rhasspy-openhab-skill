# Rhasspy-openHAB-Skill

This skill for the [Rhasspy voice assistent](https://rhasspy.readthedocs.io/en/latest/) allows you to control your [openHAB](https://www.openhab.org/) based smart home.

It is based on [Rhasspy Hermes App](https://github.com/rhasspy/rhasspy-hermes-app) by [Koen Vervloesem ](https://github.com/koenvervloesem).

## Features
* Switch items on and off in your current room
* Imports every item synonym and label as item slot at startup

## Requirements
* [Rhasspy 2.5](https://rhasspy.readthedocs.io/en/latest/)
* [openHAB 3](https://www.openhab.org/)
* [Docker](https://www.docker.com/)

Older versions may work but are not supported!

## Installation
1. Download or checkout this repository and change to that directory.

2. Build the docker image:

```Shell
docker build -t rhasspy-openhabskill .
```
3. Run the docker image:

```Shell
docker run -d --name rhasspy-openhabskill rhasspy-openhabskill
```

**Optional arguments:**

Command | Description
  ------------ | -------------
-h, --help | show this help message and exit
--openhabhost OPENHABHOST | IP of openHAB (default: localhost)
--openhabport OPENHABPORT | Port of openHAB (default: 8080)
--rhasspyhost RHASSPYHOST | IP of the Rhasspy base station (default: localhost)
--rhasspyport RHASSPYPORT | Port of the Rhasspy base station (default: 12101)
--host HOST | MQTT host (default: localhost)
--port PORT | MQTT port (default: 1883)
--username USERNAME | MQTT username
--password PASSWORD | MQTT password
--tls | Enable MQTT TLS
--tls-ca-certs TLS_CA_CERTS | MQTT TLS Certificate Authority certificate files
--tls-certfile TLS_CERTFILE | MQTT TLS client certificate file (PEM)
--tls-keyfile TLS_KEYFILE | MQTT TLS client key file (PEM)
--tls-cert-reqs {CERT_REQUIRED,CERT_OPTIONAL,CERT_NONE} | MQTT TLS certificate requirements for broker (default: CERT_REQUIRED)
--tls-version TLS_VERSION | MQTT TLS version (default: highest)
--tls-ciphers TLS_CIPHERS | MQTT TLS ciphers to use
--site-id SITE_ID | Hermes site id(s) to listen for (default: all)
--debug | Print DEBUG messages to the console
--log-format LOG_FORMAT | Python logger format

## License
This project is provided by Arne Wulf as open source software with the MIT license. See the LICENSE file for more information.