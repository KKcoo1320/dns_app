##Lab3 Authoritive server Bozhi Wang
from socket import *
## Create UDP socket
a = socket(AF_INET,SOCK_DGRAM)
a.bind(('0.0.0.0', 53533))

while True:
        data, addr = a.recvfrom(1024)
        ##decode and separate the message that received 
        cleaned_message = data.decode().strip()
        message = cleaned_message.split('\n')

        if len(message) == 4 and message[0] == "TYPE=A":
            name = message[1].split('=')[1]
            value = message[2].split('=')[1]
            ##write in dns_txt file
            with open("dns.txt", 'a') as f:
             f.write(name + "=" + value + "\n")
            a.sendto("Success".encode(), addr)

        if len(message) == 4 and message[0] == "TYPE=A":
           name = message[1].split('=')[1]
           value = message[2].split('=')[1]
           with open("dns.txt", 'a') as f:
            f.write(name + "=" + value + "\n")
            a.sendto("Success".encode(), addr)
                ##If found the record, send the response
            if len(message) == 2 and message[0] == "TYPE=A":
             name = message[1].split('=')[1]
             with open("dns.txt", 'r') as f:
              for line in f:
               record_name, record_value = line.strip().split('=')
            if record_name == name:
                response = "TYPE=A\nNAME=" + name + "\nVALUE=" + value + "\nTTL=10"
                a.sendto(response.encode(), addr)
                ##If didn't, send the not found response
            else:
                a.sendto("404: Record Not Found".encode(), addr)
         ##Send bad request response
        else:
            a.sendto("400: Bad Request".encode(), addr)