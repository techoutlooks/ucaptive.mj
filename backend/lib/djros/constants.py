# -*- coding: utf-8 -*-
__author__ = 'ceduth'


# Mikrotik/Python Type conversion mapping
ROUTEROS_BOOL = dict(true=True, false=False)


# Mikrotik CAPsMAN Caps
CAPSMAN_CAP_TYPE_INTERFACE = 'interface'                    #
CAPSMAN_CAP_TYPE_REMOTE = 'remote'                          #
CAPSMAN_GET_REMOTE_CAPS_CMD = '/caps-man/remote-cap'        # dynamic cap interfaces lookup
CAPSMAN_GET_CAPS_INTERFACES_CMD = '/caps-man/interface'     # static cap interfaces lookup
CAPSMAN_CAP_INTERFACES_LOOKUP_FIELD = 'radio_mac'           # lookup by radio_mac (default)
CAPSMAN_REMOTE_CAP_LOOKUP_FIELD = 'base_mac'                # lookup by base_mac (RemoteCap only)

# Mikrotik CAPsMAN Radios
CAPSMAN_GET_RADIOS_CMD = '/caps-man/registration-table'     # get radios
CAPSMAN_RADIOS_LOOKUP_FIELD = 'interface'                           # radios lookup field? interface:mac (used in api queries)
CAPSMAN_RADIOS_CAP_PTR_FIELD = 'name'                               # value identifies the parent cap

