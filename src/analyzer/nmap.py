import nmap

def scan(target):
    nm = nmap.PortScanner()
    nm.scan(target, '1-1024')
    return nm

result = scan('192.168.1.0/24')
print(result)