from mininet.topo import Topo
from mininet.node import OVSSwitch

class InternetTopo(Topo):
    def build(self):
        # Create a single switch
        s1 = self.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')

        # Two local hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')

        # Link them to s1
        self.addLink(h1, s1)
        self.addLink(h2, s1)

topos = {'internet': (lambda: InternetTopo())}

