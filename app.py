import os
import ipaddress
from flask import Flask
from flask import request
from merakifirewall import MerakiFirewall
from merakiapiwrapper import MerakiApiWrapper

app = Flask(__name__)

@app.route('/block/')
def block():
    ip = request.args.get('ipaddress')
    if (is_valid_ip_address(ip)): 
        meraki_api_wrapper = MerakiApiWrapper( 
            os.getenv('api_key'), 
            os.getenv('network_id')) 
        firewall = MerakiFirewall(os.getenv('src_cidr'),meraki_api_wrapper) 
        firewall.block_dest_ip(ip, 'Stealthwatch investigation') 
        return '%s blocked' % (ip)
    else:
        return 'invalid IP address provided'

def is_valid_ip_address(ip):
    try: 
        ipaddress.ip_address(ip) 
        return True
    except(ValueError):
        return False

if __name__ == "__main__": 
    app.run(host ='0.0.0.0', port = 5002, debug = True) 