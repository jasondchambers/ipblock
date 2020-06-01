
from abc import ABC, abstractmethod

# Firewall abstraction 
class Firewall(ABC):
    def block_dest_ip(self,dest_ip,comment):
        pass
