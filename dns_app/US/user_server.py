import requests
from flask import Flask, request, jsonify
from socket import *

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])

def query(as_ip,as_port,hostname):
    # Create UDP socket
    s = socket(AF_INET, SOCK_DGRAM)
    dns_query = f"TYPE=A\nNAME={hostname}"
    s.sendto(dns_query.encode(),(as_ip,as_port))
    response, _ = s.recvfrom(1024)
    return response.decode()

def fibonacci():
    # Parameters in User_server
    args = request.args
    hostname = args.get('hostname')
    fs_port = args.get('fs_port')
    number = args.get('number')
    as_ip = args.get('as_ip')
    as_port = args.get('as_port')

    # Check if any parameters missing
    if not all ([hostname, fs_port, number, as_ip, as_port]):
        return "400 Bad Request"

    fs_ip = query(as_ip, int(as_port),hostname)

## Send request to Fibonacci server
    try:
         fs_response = requests.get(f"http://{fs_ip}:{fs_port}/fibonacci?number={number}")
         return jsonify(fs_response.json()), 200
    except Exception as e:
         return "Error querying 500"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
