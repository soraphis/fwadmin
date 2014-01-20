from fwadmin.models import (
    ChangeLog
)


def log(host, user, what):
    ChangeLog(host_name=host.name,
            host_ip=host.ip,
            who=user,
            what=what).save()
