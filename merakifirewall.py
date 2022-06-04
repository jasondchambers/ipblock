"""
Implementation of a Meraki (MX) Firewall.
"""
import ipaddress
from firewall import Firewall

class MerakiFirewall(Firewall):
    """Implementation of a Meraki (MX) Firewall."""

    def __init__(self, src_cidr, meraki_api_wrapper):
        self.src_cidr = src_cidr
        self.meraki_api_wrapper = meraki_api_wrapper

    def get_rules(self):
        """Return the current L3 firewall rules"""
        return self.meraki_api_wrapper.get_rules()

    def update_rules(self, rules):
        """Update the firewall with list of rules (supplied list must exclude the default rule)"""
        self.meraki_api_wrapper.update_rules(rules)

    @staticmethod
    def strip_default_rule_from(rules):
        """Strip from the list of rules, the default rule"""
        rule_list = rules['rules']
        stripped_rule_list = list(filter(lambda rule: rule['comment'] != 'Default rule', rule_list))
        rules['rules'] = stripped_rule_list
        return rules

    @staticmethod
    def find(new_rule, rules):
        """Find new_rule in list of rules"""
        return list(filter(
            lambda existing_rule: existing_rule['destCidr'] == new_rule['destCidr'], rules))

    @staticmethod
    def rule_already_exists():
        """This method exists solely to facilitate better unit testing"""
        return

    def add_new_rule(self, rules, new_rule):
        """Add new_rule to the list of rules and update the firewall"""
        rules['rules'].append(new_rule)
        self.update_rules(rules)

    def add_rule(self, new_rule):
        """Add a rule to the firewall. The rule may already exist - that's okay"""
        rules = self.get_rules()
        rules = self.strip_default_rule_from(rules)
        rule_already_exists = self.find(new_rule, rules['rules'])
        if not rule_already_exists:
            self.add_new_rule(rules, new_rule)
        else:
            self.rule_already_exists()

    def block_cidr(self, dest_cidr, comment):
        """Block a CIDR (Meraki MX rules are based on CIDRs rather than explicit IP addresses.)"""
        new_rule = {
            'comment': comment,
            'destCidr': dest_cidr,
            'destPort': 'Any',
            'policy': 'deny',
            'protocol': 'any',
            'srcCidr': self.src_cidr,
            'srcPort': 'Any',
            'syslogEnabled': 'false'
        }
        self.add_rule(new_rule)

    @staticmethod
    def invalid_input():
        """This method exists solely to facilitate better unit testing"""
        return

    @staticmethod
    def is_valid_ip_address(ip_address):
        """Returns True if ip_address is a valid IPv4 or IPv6 address."""
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False

    def block_dest_ip(self, dest_ip, comment):
        if self.is_valid_ip_address(dest_ip):
            self.block_cidr(dest_ip+'/32', comment)
        else:
            self.invalid_input()
