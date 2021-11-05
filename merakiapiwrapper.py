"""
Wrapper for the Meraki Dashboard API.
"""
import meraki

class MerakiApiWrapper():
    """Wrapper for the Meraki Dashboard APIs."""

    def __init__(self, api_key, network_id):
        self.api_key = api_key
        self.network_id = network_id
        self.dashboard = meraki.DashboardAPI(
            api_key=api_key,
            output_log=False)

    def get_rules(self):
        """Get the rules from the firewall."""
        return self.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(self.network_id)

    def update_rules(self, rules):
        """Upddate the rules in the firewall."""
        response = self.dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(self.network_id,rules=rules['rules'])
