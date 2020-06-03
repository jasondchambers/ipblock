"""
The main Flask application.
"""
import os
from flask import Flask
from flask import request
from merakifirewall import MerakiFirewall
from merakiapiwrapper import MerakiApiWrapper

app = Flask(__name__)

@app.route('/block/')
def block():
    """Block the specified IP"""
    ip_address = request.args.get('ipaddress')
    if MerakiFirewall.is_valid_ip_address(ip_address):
        meraki_api_wrapper = MerakiApiWrapper(
            os.getenv('api_key'),
            os.getenv('network_id'))
        firewall = MerakiFirewall(os.getenv('src_cidr'), meraki_api_wrapper)
        firewall.block_dest_ip(ip_address, 'Stealthwatch investigation')
        return '%s blocked' % (ip_address)
    return 'invalid IP address provided'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
