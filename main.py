import sys
import re
from modules.scan_profile import get_scan_type
from modules.dns_enum import run as dns_run
from modules.analyzer import analyze_target
from modules.report_gen import save_report
from modules.nmap_scan import run as nmap_run
from modules.webtech_detect import detect_technologies
from modules.dirb import run as dirb_run

def is_ip(address):
    pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    if re.match(pattern, address):
        parts = address.split(".")
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    return False

def ask_dns_port():
    use_custom = input("Souhaitez-vous utiliser un port DNS personnalisé ? (y/N) ").strip().lower()
    if use_custom == 'y':
        try:
            port = int(input("Entrez le port DNS à utiliser : ").strip())
            if 1 <= port <= 65535:
                return port
            else:
                print("[!] Port invalide. Utilisation du port par défaut (53).")
        except ValueError:
            print("[!] Entrée non valide. Utilisation du port par défaut (53).")
    return 53

def main():
    target = input("Entrez la cible à analyser (IP ou domaine) : ").strip()
    if not target:
        print("Erreur : cible vide.")
        sys.exit(1)

    do_nmap = input("Voulez-vous lancer un scan Nmap ? (y/N) ").strip().lower()
    nmap_output = ""
    scan_args = []
    if do_nmap == 'y':
        print("\nChoisissez le type de scan Nmap :")
        print("1) Scan SYN (-sS), version (-sV) et OS (-O)")
        print("2) Scan complet ports (-p-) et version (-sV)")
        print("3) Scan rapide (-F)")
        print("4) Scan agressif (-A)")
        print("5) Options personnalisées")
        scan_choice = input("Votre choix (1-5) : ").strip()

        scan_args = get_scan_type(scan_choice)
        nmap_output = nmap_run(target, scan_args)
    else:
        print("[Nmap] Scan Nmap sauté par l'utilisateur.")

    dns_results = {
        'dns': {},
        'zone_transfer': {},
        'subdomains_found': [],
        'whois': {}
    }
    if not is_ip(target):
        do_dns = input("Voulez-vous lancer un scan DNS ? (y/N) ").strip().lower()
        if do_dns == 'y':
            print("[DNS] Analyse DNS...")
            dns_port = ask_dns_port()
            dns_results = dns_run(target, port=dns_port)
        else:
            print("[DNS] Scan DNS sauté par l'utilisateur.")
    else:
        print("[DNS] Cible détectée comme IP, saut de l'analyse DNS.")

    dirb_pages = []
    do_dirb = input("Voulez-vous lancer un scan dirb sur la cible ? (y/N) ").strip().lower()
    if do_dirb == 'y':
        dirb_pages = dirb_run(target)
        print(f"[dirb] Pages web trouvées : {dirb_pages}")

    results = analyze_target(target, scan_args, dns_results, dirb_pages=dirb_pages, nmap_output=nmap_output)

    results['dns'] = dns_results
    results['nmap'] = nmap_output

    save_report(target, results)

    print("\nAnalyse terminée !")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompu par l'utilisateur.")
        sys.exit(0)
