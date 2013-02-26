import json

i = 0
for line in open("/etc/services").readlines():
    line = line.strip()
    if line.startswith("#") or not line:
        continue
    name, port_and_type = line.split()[:2]
    port, type = port_and_type.split("/")
    d = {"model": "fwadmin.port",
         "pk": i,
         "fields": {
            "name": name,
            "number": port,
            "type": type.upper()
            }
         }
    print json.dumps(d) + ","
    i += 1
