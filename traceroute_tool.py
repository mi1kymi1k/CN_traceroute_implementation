import socket # for DNS resolution 
import time # for time related functions
import argparse # for parsing command-line arguments 
import random
from scapy.all import sr1 # packet manipulation library 
from scapy.layers.inet import IP, UDP # protocal layer classes to avoid undefined symbol warnings in IDE


# traceroute function 
def traceroute(destination, max_hops=20, timeout=2):
    destination_ip = socket.gethostbyname(destination) # resolves the destination host to its IP address using DNS
    dest_port = random.randint(33434, 33464) # port destinations for traceroute 
    source_port = random.randint(49152, 65535) # port source for traceroute
    ttl = 1

    # printing information
    print(f"traceroute to {destination} ({destination_ip}), {max_hops} hops max, {timeout} seconds timeout")

    # enter a loop, incrementing the TTL for each iteration, and sends UDP packets to the destination using Scapy.  
    while ttl <= max_hops:
        # creating the IP and UDP headers 
        ip_packet = IP(dst=destination, ttl=ttl)
        udp_packet = UDP(sport=source_port, dport=dest_port)

        # combining the headers 
        packet = ip_packet / udp_packet

        start = time.time()
        # sending the packet and receive a reply 
        reply = sr1(packet, timeout=timeout, verbose=0)
        end = time.time()

        # interpret the responses and print information about each hop (router) or timeout.
        if reply is None: 
            # no reply, print * for timeout 
            print (f'{ttl} *')
        else: 
            # destination reached, print the details
            rtt_ms = (end - start) * 1000
            print (f"{ttl} {reply.src} {rtt_ms:.3f} ms")

            if reply.type == 3 and reply.code == 3: # ICMP type 3 indicates destination unreachable, which means the destination is reached 
                break

        # increments the TTL for each iteration and breaks out of the loop when the destination is reached or the TTL exceeds the specified maximum hops. 
        ttl += 1

# main function 
def main():
    # argument passing 
    # utilizes the argeparse library to parse command-line arguments. defining 3 args: destination (the target host or IP address), max-hops (maximum number of hops), and timeout(timeout for each packet)
    parser = argparse.ArgumentParser(description="Traceroute implementaion in Python")
    parser.add_argument("destination", help="Destination host or IP address")
    args = parser.parse_args() 

    # calling traceroute function 
    # calls the traceroute function with the provided arguments 
    traceroute(args.destination, max_hops=args.max_hops, timeout=args.timeout)


# script execution
if __name__ == "__main__":
    main()