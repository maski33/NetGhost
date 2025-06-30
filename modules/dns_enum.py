# modules/dns_enum.py

import dns.resolver
import dns.zone
import dns.query
import whois as whois_module

def query_dns(domain, record_type, port=53, nameserver=None):
    try:
        resolver = dns.resolver.Resolver()
        if nameserver:
            resolver.nameservers = [nameserver]
        resolver.port = port
        answers = resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except Exception as e:
        return [f"Erreur lors de la requête {record_type}: {e}"]

        
def test_zone_transfer(ns_server, domain, port=53):
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(ns_server, domain, port=port, timeout=5))
        if zone:
            return [str(node) for node in zone.nodes.keys()]
    except Exception:
        return []
    return []

def brute_subdomains(domain, wordlist):
    found = []
    for sub in wordlist:
        try:
            fqdn = f"{sub}.{domain}"
            answers = dns.resolver.resolve(fqdn, 'A')
            if answers:
                found.append(fqdn)
        except Exception:
            pass
    return found

def run(target, port=53):
    print(f"Enumération DNS et WHOIS sur {target} (port {port})...")

    dns_results = {}
    for record in ['A', 'AAAA', 'MX', 'NS', 'TXT']:
        dns_results[record] = query_dns(target, record)

    zone_transfers = {}
    if 'NS' in dns_results:
        for ns in dns_results['NS']:
            print(f"Test de zone transfer sur {ns} ...")
            zone_transfers[ns] = test_zone_transfer(ns, target, port=port)
            if zone_transfers[ns]:
                print(f"Zone transfer possible sur {ns} - enregistrements récupérés : {len(zone_transfers[ns])}")
            else:
                print(f"Zone transfer non autorisé sur {ns}")

    wordlist = ['admin', 'test', 'mail', 'dev', 'webmail', 'ftp']
    print(f"Bruteforce sous-domaines avec {len(wordlist)} mots...")
    subdomains_found = brute_subdomains(target, wordlist)
    if subdomains_found:
        print(f"Sous-domaines trouvés : {subdomains_found}")
    else:
        print(f"Aucun sous-domaine trouvé avec la wordlist.")

    try:
        w = whois_module.whois(target)
        whois_info = {key: w[key] for key in ['domain_name', 'registrar', 'creation_date', 'expiration_date', 'name_servers'] if key in w}
    except Exception as e:
        whois_info = f"Erreur WHOIS : {e}"

    return {
        'dns': dns_results,
        'zone_transfer': zone_transfers,
        'subdomains_found': subdomains_found,
        'whois': whois_info
    }
