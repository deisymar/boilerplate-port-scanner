import socket
import re

from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    ip = ''
    open_ports = []

    try:
        ip = socket.gethostbyname(target)
        for port in range(port_range[0], port_range[1] + 1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            # returns an error indicator
            result = s.connect_ex((ip, port))
            if result == 0:
                #print("Port {} is open".format(port))
                open_ports.append(port)

            s.close()

    except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
    except socket.gaierror:
        if (re.search('[a-zA-Z]', target)):
            return ("Error: Invalid hostname")
        return ("Error: Invalid IP address")
    except socket.error:
        return ("Error: Invalid IP address")

    host = None
    try:
        host = socket.gethostbyaddr(ip)[0]
    except socket.error:
        host = None

    final_string = "Open ports for"
    if host != None:
        final_string += " {url} ({ip})".format(url=host, ip=ip)
    else:
        final_string += " {ip}".format(ip=ip)
    final_string += "\n"
    if verbose:
        header = "PORT     SERVICE\n"
        body = ""
        #use the dictionary in common_ports.py to get the correct service name
        #for each port
        for port in open_ports:
            if port in ports_and_services:
                service = ports_and_services[port]
            else:
                service = ''

            port_str = str(port).ljust(9, ' ')
            #body += "{p}".format(p=port) + " " * (9 - len(str(port))) + "{sn}".format(                    sn=socket.getservbyport(port))
            body += "{p}".format(p=port_str) + "{sn}".format(sn=service)

            if (open_ports[len(open_ports) - 1] != port):
                body += "\n"
        return final_string + header + body

    return (open_ports)
