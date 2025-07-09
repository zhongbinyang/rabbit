import ipaddress
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_ip(ip):
    try:
        # macOS/Linux: -c 1 只发1个包，-W 1 超时1秒
        result = subprocess.run([
            'ping', '-c', '1', '-W', '1', str(ip)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return str(ip) if result.returncode == 0 else None
    except Exception:
        return None

def scan_network(network_cidr, max_workers=64):
    net = ipaddress.ip_network(network_cidr, strict=False)
    ips = list(net.hosts())
    reachable = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {executor.submit(ping_ip, ip): ip for ip in ips}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            res = future.result()
            if res:
                print(f"可达: {res}")
                reachable.append(res)
    return reachable

def main():
    if len(sys.argv) < 2:
        print("用法: python testip.py 192.168.1.0/24")
        sys.exit(1)
    network_cidr = sys.argv[1]
    print(f"扫描网段: {network_cidr}")
    reachable = scan_network(network_cidr)
    print("\n可达IP列表:")
    for ip in reachable:
        print(ip)

if __name__ == "__main__":
    main()
