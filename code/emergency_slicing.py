from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import subprocess
import time

class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)

        # Destination Mapping [router --> MAC Destination --> Eth Port Output]
        self.mac_to_port = {
            1: {"00:00:00:00:00:01": 2, "00:00:00:00:00:02": 3, "00:00:00:00:00:03": 4, "00:00:00:00:00:04": 1, "00:00:00:00:00:05": 1, "00:00:00:00:00:06": 1},
            2: {"00:00:00:00:00:04": 2, "00:00:00:00:00:05": 3, "00:00:00:00:00:06": 4, "00:00:00:00:00:01": 1, "00:00:00:00:00:02": 1, "00:00:00:00:00:03": 1},
        }        
       
        self.emergency = 0          # Boolean that indicates the presence of an emergency scenario
        self.time = time.time()     # Timer that keeps track of time for an emergency scenario
        self.print_flag = 0         # Helper variable that helps us with printing/output
              
        # Source Mapping        
        self.port_to_port = {
            1: {2:1, 3:1, 4:1},
            2: {2:1, 3:1, 4:1},
        }
        self.end_swtiches = [1, 4]
    
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)
        ]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match, instructions=inst
        )
        datapath.send_msg(mod)

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        in_port = msg.match["in_port"]

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        
        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        
        if dpid in self.mac_to_port:
            if (self.emergency == 1): 
                if dst in self.mac_to_port[dpid]:
                    out_port = self.mac_to_port[dpid][dst]
                    actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                    match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                    self.add_flow(datapath, 1, match, actions)
                    self._send_package(msg, datapath, in_port, actions)

            else:                    
                if dst in self.mac_to_port[dpid]:
                    out_port = self.mac_to_port[dpid][dst]
                    actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                    match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                    self.add_flow(datapath, 1, match, actions)
                    self._send_package(msg, datapath, in_port, actions)
   
    def run(self):
        while True:
            print("\nMenu:")
            print("1. Modalità Normale")
            print("2. Modalità Emergenza")
            print("3. Modalità Personalizzata")
            print("4. Esci")
            choice = input("Seleziona un'opzione: ")

            if choice == '1':
                self.normal_mode()
                subprocess.call(["python3","./print_network.py", "a"])
            elif choice == '2':
                self.emergency_mode()
                subprocess.call(["python3","./print_network.py", "b"])
            elif choice == '3':
                choice2 = input("Seleziona la slice da attivare: ")
                if choice2 == "1":
                    self.pers_mode("a")
                    subprocess.call(["python3","./print_network.py", "c1"])
                elif choice2 == "2":
                    self.pers_mode("b")
                    subprocess.call(["python3","./print_network.py", "c2"])
                elif choice2 == "3":
                    self.pers_mode("c")
                    subprocess.call(["python3","./print_network.py", "c3"])
                else:
                    print("Opzione non valida. Riprova.")
            elif choice == "4":
                print("Arrivederci!")    
                break
            else:
                print("Opzione non valida. Riprova.")

    def normal_mode(self):
        print("\nModalità Normale attivata")
        subprocess.call("./common_scenario.sh")

    def emergency_mode(self):
        print("\nModalità Emergenza attivata")
        subprocess.call("./sos_scenario.sh")  

    def pers_mode(self, slice):
        print("\nModalità Personalizzata attivata")
        subprocess.call(['./scenario_personalizzato.sh', slice])                    
                