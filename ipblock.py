import meraki
import json

class IpBlocker:

    def __init__(self, api_key, network_id, src_cidr):
        self.api_key = api_key
        self.network_id = network_id
        self.src_cidr = src_cidr
        self.dashboard = meraki.DashboardAPI( 
            api_key=api_key, 
            base_url='https://api-mp.meraki.com/api/v0/',
            output_log=False) 
            
    def strip_default_rule_from(self,rules): 
        return list(filter(lambda rule: rule['comment'] != 'Default rule', rules))

    def find(self,new_rule,rules): 
        return list(filter(lambda existing_rule: existing_rule['destCidr'] == new_rule['destCidr'], rules))

    def add_rule(self,new_rule): 
        mx_l3_firewall = self.dashboard.mx_l3_firewall
        rules = mx_l3_firewall.getNetworkL3FirewallRules(self.network_id) 
        rules = self.strip_default_rule_from(rules)
        rule_already_exists = self.find(new_rule,rules)
        if not rule_already_exists: 
            print ('Adding new rule') 
            rules.append(new_rule) 
            response = mx_l3_firewall.updateNetworkL3FirewallRules(self.network_id,rules=rules) 
        else: 
            print('Rule already exists')

    def block_cidr(self,dest_cidr, comment): 
        new_rule = { 
            'comment': comment,
            'destCidr': dest_cidr,
            'destPort': 'Any', 
            'policy': 'deny', 
            'protocol': 'tcp', 
            'srcCidr': self.src_cidr,
            'srcPort': 'Any', 
            'syslogEnabled': 'false' 
        }
        self.add_rule(new_rule)

    def block_dest_ip(self,dest_ip, comment):
        self.block_cidr(dest_ip+'/32', comment)

