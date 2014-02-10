import netaddr

from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_port(port_range):
    # validate port_range
    start, sep, end = port_range.replace(" ", "").partition("-")
    if not start.isdigit():
        raise ValidationError(
            _("Port or Range must be a single port or a range."))
    if end and not end.isdigit():
        raise ValidationError(_("End port must be a number"))
    if int(start) > 65535 or (end and int(end) > 65535):
        raise ValidationError(
            _("Port can not be greater than 65535"))
    if end and int(start) >= int(end):
        raise ValidationError(
            _("Port order incorrect"))


def validate_from_net(from_net):
    if from_net and from_net != "any":
        try:
            net = netaddr.IPNetwork(from_net)
            net  # pyflakes
        except netaddr.AddrFormatError:
            raise ValidationError(_("Invalid network address"))
