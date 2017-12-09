from __future__ import division
from operator import attrgetter

import shortest_route
from ryu.base import app_manager
#ryu.controller.event.EventBase
from ryu.controller import event
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import hub
#from shortest_route import *
'''
ggg
class Access_Control(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _NAME = 'Access_Control'

    def __init__(self, *args, **kwargs):
        super(Access_Control, self).__init__(*args, **kwargs)

        self.name = 'Access_Control'
        self.logger.info("----############### ACCESS CONTROL:  -----")
        hery=
        self.logger.info("----############### ACCESS CONTROL hery:  %s-----",hery)


'''