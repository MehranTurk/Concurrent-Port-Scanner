import socket
import concurrent.futures
from tqdm import tqdm
import threading

open_ports = []
lock = threading.Lock()

important_ports = [80, 443, 22, 25, 110, 143, 445, 3389, 23, 21, 37, 42, 53, 67, 68, 69, 70, 79, 81, 88, 98, 109, 110, 123, 135, 137, 138, 139, 143, 161, 162, 177, 177, 256, 164, 389, 500, 512, 513, 514, 515, 517, 520, 540, 593, 631, 636, 898, 901, 1025, 1039, 1080, 1352, 1433, 1434, 1494, 1512, 1521, 2049, 301, 2381, 2401, 3128, 3265, 3269, 3306, 3389, 4045, 5987, 5631, 5632, 5800, 6000, 6255, 7100, 8000, 8001, 8002, 8080, 8081, 8888, 32770, 32899, 49400, 49401, ]

def scan_port(ip_address, port):
    global open_ports
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)  # تنظیم زمان انتظار برای اتصال به پورت
        result = s.connect_ex((ip_address, port))
        s.close()
        if result == 0:
            with lock:
                open_ports.append(port)
            return port
        else:
            return None
    except:
        return None

def port_scan(ip_address):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(lambda port: scan_port(ip_address, port), important_ports), total=len(important_ports), desc="Scanning Ports", unit="port"))
    
    open_ports.sort()
    if len(open_ports) == 0:
        print("No open ports found.")
    else:
        print("Open ports:", open_ports)

if __name__ == "__main__":
    ip_address = input("Enter the IP address to scan: ")
    port_scan(ip_address)
