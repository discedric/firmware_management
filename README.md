# Netbox firmware Plugin

Een [Netbox](https://github.com/netbox-community/netbox) plugin voor het bijhouden van de firmwares en bios van de apparaten
Dit is een plugin geschreven door een student tijdens een stage dus tijdelijke updates kunnen nog gebeuren tijdens de geduurte van deze stage.

## Features

Een plugin voor het bijhouden van de firmware en bios versies die op uw devices, modules en inventory items staan.
Dit is een simpele plugin die een basis legt voor eigen uitbreidingen

## Compatibility
| Netbox Version | Plugin Version |
|----------------|----------------|
|       4.2      |      1.0.0     |

## Installing

Officiele installeer instructies: [official Netbox plugin documentation](https://docs.netbox.dev/en/stable/plugins/#installing-plugins)
Je zal ook de plugin [netbox-inventory](https://github.com/ArnesSI/netbox-inventory) moeten installeren omdat we deze gebruiken.

Je kan de plugin installeren via de github cli of via git
```bash
$ source /opt/netbox/venv/bin/activate
(venv) $ cd /opt/netbox/netbox/netbox/plugins
(venv) $ gh repo clone discedric/netbox_firmware
(venv) $ pip install ./netbox_firmware
```

```python
PLUGINS = [
    'netbox_firmware'
]
```

Je zal ook moeten database migrations en netbox search index moeten updaten:

```bash
(venv) $ cd /opt/netbox/netbox/
(venv) $ python3 manage.py migrate
(venv) $ python3 manage.py reindex --lazy
```

