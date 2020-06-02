import unittest
from merakiapiwrapper import MerakiApiWrapper
from unittest.mock import patch, Mock, MagicMock
from merakifirewall import MerakiFirewall

class MerakiFirewallTestCase(unittest.TestCase):

    @patch('merakifirewall.MerakiFirewall.rule_already_exists')
    @patch('merakifirewall.MerakiFirewall.update_rules')
    @patch('merakifirewall.MerakiFirewall.get_rules')
    def test_block_dest_ip_already_blocked(self,mock_get_rules,mock_update_rules,mock_rule_already_exists):
        src_cidr = '192.168.128.0/24' 
        ipaddress = '54.222.60.219' 
        meraki_api_wrapper = MagicMock()
        firewall = MerakiFirewall(src_cidr,meraki_api_wrapper)
        mock_get_rules.return_value=[ 
            {
                'comment': 'Unit Testing', 
                'policy': 'deny', 
                'protocol': 'any', 
                'srcPort': 'Any', 
                'srcCidr': '192.168.128.0/24', 
                'destPort': 'Any', 
                'destCidr': '54.222.60.219/32', 
                'syslogEnabled': True
            }, 
            {
                'comment': 'Default rule', 
                'policy': 'allow', 
                'protocol': 'Any', 
                'srcPort': 'Any', 
                'srcCidr': 'Any', 
                'destPort': 'Any', 
                'destCidr': 'Any', 
                'syslogEnabled': False
            }
        ]
        firewall.block_dest_ip(ipaddress, 'Testing')
        mock_rule_already_exists.assert_called_with()

    @patch('merakifirewall.MerakiFirewall.invalid_input')
    def test_block_invalid_ip(self,mock_invalid_input):
        src_cidr = '192.168.128.0/24' 
        invalid_ipaddress = '5jsdk4.2djffdj22.6fjdjf0.220' 
        meraki_api_wrapper = MagicMock()
        firewall = MerakiFirewall(src_cidr,meraki_api_wrapper)
        firewall.block_dest_ip(invalid_ipaddress, 'Testing')
        assert mock_invalid_input.called

    @patch('merakifirewall.MerakiFirewall.add_new_rule')
    @patch('merakifirewall.MerakiFirewall.update_rules')
    @patch('merakifirewall.MerakiFirewall.get_rules')
    def test_block_new_dest_ip(self,mock_get_rules,mock_update_rules,mock_add_new_rule):
        src_cidr = '192.168.128.0/24' 
        ipaddress = '54.222.60.220' 
        meraki_api_wrapper = MagicMock()
        firewall = MerakiFirewall(src_cidr,meraki_api_wrapper)
        existing_rule = {
            'comment': 'Unit Testing', 
            'policy': 'deny', 
            'protocol': 'any', 
            'srcPort': 'Any', 
            'srcCidr': '192.168.128.0/24', 
            'destPort': 'Any', 
            'destCidr': '54.222.60.219/32', 
            'syslogEnabled': True
        } 
        mock_get_rules.return_value=[ 
            existing_rule,
            {
                'comment': 'Default rule', 
                'policy': 'allow', 
                'protocol': 'Any', 
                'srcPort': 'Any', 
                'srcCidr': 'Any', 
                'destPort': 'Any', 
                'destCidr': 'Any', 
                'syslogEnabled': False
            }
        ]
        firewall.block_dest_ip(ipaddress, 'Testing')
        expected_new_rule = {
            'comment': 'Testing', 
            'destCidr': '54.222.60.220/32', 
            'destPort': 'Any', 
            'policy': 'deny', 
            'protocol': 'any', 
            'srcCidr': '192.168.128.0/24', 
            'srcPort': 'Any', 
            'syslogEnabled': 'true' 
        }
        mock_add_new_rule.assert_called_with([existing_rule], expected_new_rule)