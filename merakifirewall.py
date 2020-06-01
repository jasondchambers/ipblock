import merakiapiwrapper
import json
from firewall import Firewall

class MerakiFirewall(Firewall):

    def __init__(self, src_cidr, meraki_api_wrapper):
        self.src_cidr = src_cidr
        self.meraki_api_wrapper = meraki_api_wrapper

    def get_rules(self):
        return self.meraki_api_wrapper.get_rules()

    def update_rules(self,rules):
        self.meraki_api_wrapper.update_rules(rules)

    def strip_default_rule_from(self,rules): 
        return list(filter(lambda rule: rule['comment'] != 'Default rule', rules))

    def find(self,new_rule,rules): 
        return list(filter(lambda existing_rule: existing_rule['destCidr'] == new_rule['destCidr'], rules))

    def rule_already_exists(self):
        return

    def add_new_rule(self,rules,new_rule):
        rules.append(new_rule) 
        self.update_rules(rules)

    def add_rule(self,new_rule): 
        rules = self.get_rules()
        rules = self.strip_default_rule_from(rules)
        rule_already_exists = self.find(new_rule,rules)
        if not rule_already_exists: 
            self.add_new_rule(rules,new_rule)
        else: 
            self.rule_already_exists()

    def block_cidr(self,dest_cidr, comment): 
        new_rule = { 
            'comment': comment,
            'destCidr': dest_cidr,
            'destPort': 'Any', 
            'policy': 'deny', 
            'protocol': 'any', 
            'srcCidr': self.src_cidr,
            'srcPort': 'Any', 
            'syslogEnabled': 'true' 
        }
        self.add_rule(new_rule)

    def block_dest_ip(self,dest_ip, comment):
        self.block_cidr(dest_ip+'/32', comment)

