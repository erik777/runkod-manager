from dns.exception import DNSException
from dns.resolver import Resolver, NXDOMAIN

resolver = Resolver()


def is_domain_exists(name: str) -> bool:
    try:
        resolver.query(name, 'A')
    except NXDOMAIN:
        return False
    except Exception:
        pass

    return True


def get_txt_records(name: str) -> list:
    try:
        answers = resolver.query(name, 'TXT')
        return list(set([x.to_text().strip().rstrip('"').lstrip('"') for x in answers]))
    except DNSException:
        return []


def get_a_records(name: str) -> list:
    try:
        answers = resolver.query(name, 'A')
        return list(set([x.to_text().strip() for x in answers]))
    except DNSException:
        return []
