import socket
import os
import subprocess
import platform
import re

# 预设允许的设备 IP 和口令
allowed_ip = YOUR_MAC_ADDR
secret_token = YOUR_TOKEN

def get_mac_address_robust(ip_address):
    system = platform.system()
    mac_address = None
    
    try:
        # 尝试多种命令来获取ARP信息
        commands = []
        
        if system == "Windows":
            commands = [['arp', '-a']]
        elif system == "Linux":
            commands = [['arp', '-n'], ['ip', 'neigh']]
        elif system == "Darwin":
            commands = [['arp', '-a']]
        
        for cmd in commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
                output = result.stdout
                
                # 多种MAC地址格式的正则表达式
                mac_patterns = [
                    r'([0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2})',
                    r'([0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4})'  # Cisco格式
                ]
                
                for line in output.split('\n'):
                    if ip_address in line:
                        for pattern in mac_patterns:
                            match = re.search(pattern, line, re.IGNORECASE)
                            if match:
                                mac_address = match.group(1)
                                # 统一格式为冒号分隔
                                if '-' in mac_address:
                                    mac_address = mac_address.replace('-', ':')
                                return mac_address.upper()  # 返回大写的MAC地址
                
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
                
    except Exception as e:
        print(f"Error getting MAC address: {e}")
    
    return mac_address

def lock_computer():
    print("Lock command received, locking now...")
    os.system("rundll32.exe user32.dll,LockWorkStation")

def main():
    global allowed_ip

    # 创建 UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # 允许接收广播
    sock.bind(("", 7834))  # 绑定所有网卡，端口 7834

    print("Listening for UDP broadcasts on port 7834...")

    while True:
        data, addr = sock.recvfrom(1024)  # 接收数据
        sender_mac = get_mac_address_robust(addr[0])
        sender_mac = str(sender_mac)
        print(sender_mac)
        message = data.decode(errors="ignore").strip()
        print(f"Received from {sender_mac}: {message}")

        if message == secret_token:
            if sender_mac == allowed_ip:
                lock_computer()
            else:
                print("Unauthorized device tried to lock!")

if __name__ == "__main__":
    main()
