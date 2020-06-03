"""
The Firewall base-class captures the essential behaviors of all Firewalls in
this particular context.
"""
from abc import ABC

class Firewall(ABC):
    """Base Firewall class designed for all possible firewall implementations."""
    def block_dest_ip(self, dest_ip, comment):
        """ddd"""
        pass
