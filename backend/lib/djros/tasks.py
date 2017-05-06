# -*- coding: utf-8 -*-
__author__ = 'ceduth'


from apps.orgs.tasks import OrgTask
from .settings import get_setting


class SyncCapsMan(OrgTask):
    """ 
    Keep db update  with data from CAPsMAN every 'settings.ORG_TASK_TIMEOUT' minutes. 
    
    """
    def org_task(self, org):
        """ Syncs org CAPsMAN with local database """

        active_capsmans = org.capsmans.active()
        if not active_capsmans:
            self.log_info(org, "No active CAPsMAN for org {org}. Exiting.")
        else:
            self.log_info(org, "Syncing CAPs & radios for {count} active CAPsMAN at {org} ...", count=active_capsmans.count())

            for capsman in active_capsmans:
                caps_total_count = capsman.caps.enabled().count() if get_setting('CAPSMAN_SYNC_ENABLED_CAPS_ONLY') else capsman.caps.count()
                self.log_info(org, "Syncing CAPs & radios for CAPsMAN {name} ({ip_addr}) ...", name=capsman.name, ip_addr=capsman.ip_addr)

                # sync caps
                # FIXME: proper task result/msg to OrgTask handler
                caps_sync_count = capsman.sync_interface_caps()
                self.log_info(org, "Done ..... Synced {count}/{total} CAPs.", count=caps_sync_count, total=caps_total_count)

                # sync radios
                radios_sync_count = capsman.sync_radios()
                self.log_info(org, "Done ..... Synced {count} radios.", count=radios_sync_count)
