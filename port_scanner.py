import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

# Port scan function
def scan_port(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))
        try:
            banner = sock.recv(1024).decode().strip()
        except:
            banner = "No banner"
        return (port, "OPEN", banner)
    except:
        return None

def run_scanner(ip, ports):
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: scan_port(ip, p), ports)
        for result in results:
            if result:
                open_ports.append(result)
    return open_ports

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Python Port Scanner")
    parser.add_argument("target", help="Target IP or domain to scan")
    parser.add_argument("--start", type=int, default=1, help="Start port")
    parser.add_argument("--end", type=int, default=1024, help="End port")
    args = parser.parse_args()

    print(f"Scanning {args.target} from port {args.start} to {args.end}...\n")
    ports = list(range(args.start, args.end + 1))
    results = run_scanner(args.target, ports)

    for port, status, banner in results:
        print(f"[+] Port {port} is {status} - Banner: {banner}")
