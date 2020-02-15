from dns.exception import DNSException
from dns.resolver import Resolver, NXDOMAIN

resolver = Resolver()


def is_domain_exists(name: str) -> bool:
    try:
        resolver.query(name, 'A')
    except NXDOMAIN:
        return False
    else:
        pass

    return True


def get_txt_records(name: str) -> list:
    try:
        answers = resolver.query(name, 'TXT')
        txt_records = list(set([x.to_text().strip().rstrip('"').lstrip('"') for x in answers]))
        return txt_records
    except DNSException:
        return []
