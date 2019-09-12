import socket


def domain_ip(domain: str) -> str:
    return socket.gethostbyname(domain)
