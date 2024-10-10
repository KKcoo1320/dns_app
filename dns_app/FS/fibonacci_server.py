from flask import Flask, request, jsonify
from socket import *

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    ##Request json data
    data = request.json
    keys = ['hostname', 'ip', 'as_ip', 'as_port']
    for key in keys:
        if key not in data:
         keys.append(key)
    hostname = data['hostname']
    Fip = data['ip']
    as_ip = data['as_ip']
    as_port = int(data['as_port'])
    ## Send message to file 
    message = "TYPE=A\n" + "NAME=" + hostname + "\n" + "VALUE=" + Fip + "\n" + "TTL=10"

## Send message to Auth_server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as host:
            host.sendto(message.encode(), (as_ip, as_port))
        return "201 Registered successfully"
    except Exception as e:
        return "Error registering 500"

@app.route('/fibonacci', methods=['GET'])
def request_fibonacci():
    number = request.args.get('number')
    if not number or not number.isnumeric():
        return "400 Bad Request"
##Calculate fibonacci sequence
    result = fibonacci(number)
    return jsonify({"200 OK result": result})

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)

