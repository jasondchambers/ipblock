import os
from flask import Flask
from flask import request
from ipblock import IpBlocker

app = Flask(__name__)

@app.route('/block/')
def block():
    ipaddress = request.args.get('ipaddress')
    ip_blocker = IpBlocker(
        os.getenv('api_key'),
        os.getenv('network_id'),
        os.getenv('src_cidr'))
    ip_blocker.block_dest_ip(ipaddress, 'Stealthwatch investigation')
    return '%s blocked' % (ipaddress)

if __name__ == "__main__": 
    app.run(host ='0.0.0.0', port = 5002, debug = True) 