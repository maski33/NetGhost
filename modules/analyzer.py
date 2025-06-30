from modules import webtech_detect, nmap_scan

def analyze_target(target, scan_args, dns_data, dirb_pages=None, nmap_output=""):
    if dirb_pages is None:
        dirb_pages = []

    print(f"\n[+] Lancement de l'analyse complète pour : {target}")
    findings = []

    print("[DNS] Analyse DNS...")

    if dns_data['zone_transfer'] and any(dns_data['zone_transfer'].values()):
        findings.append("[!] Zone transfer possible - risque DNS majeur")
    
    if dns_data['subdomains_found']:
        findings.append(f"[+] Sous-domaines découverts : {', '.join(dns_data['subdomains_found'])}")

    if isinstance(dns_data['whois'], dict):
        registrar = dns_data['whois'].get('registrar')
        exp = dns_data['whois'].get('expiration_date')
        if registrar:
            findings.append(f"[*] Registrar : {registrar}")
        if exp:
            findings.append(f"[*] Expiration du domaine : {exp}")


    print("[WEB] Détection des technologies web...")
    url = f"http://{target}"
    tech_data = webtech_detect.detect_technologies(url)

    if tech_data:
        if tech_data.get('cms'):
            findings.append(f"[+] CMS détecté : {', '.join(tech_data['cms'])}")
        if tech_data.get('frameworks'):
            findings.append(f"[*] Frameworks : {', '.join(tech_data['frameworks'])}")
        if tech_data.get('languages'):
            findings.append(f"[*] Langages backend : {', '.join(tech_data['languages'])}")
        if tech_data.get('server'):
            findings.append(f"[*] Serveur web : {tech_data['server']}")
        if tech_data.get('x_powered_by'):
            findings.append(f"[*] X-Powered-By : {tech_data['x_powered_by']}")

    print("[NMAP] Analyse des résultats du scan Nmap...")

    if nmap_output:
        open_ports = []
        for line in nmap_output.splitlines():
            if "/tcp" in line or "/udp" in line:
                if "open" in line:
                    open_ports.append(line.strip())
        if open_ports:
            findings.append(f"[+] Ports ouverts :\n  - " + "\n  - ".join(open_ports))
        else:
            findings.append("[-] Aucun port ouvert détecté.")
    else:
        findings.append("[-] Aucun résultat Nmap fourni.")

    if dirb_pages:
        findings.append(f"[+] Pages web découvertes par dirb : {len(dirb_pages)}")
        for url, code in dirb_pages:
            findings.append(f"    - {url} (HTTP {code})")

    print("\n========== Synthèse de l'analyse ==========")
    for f in findings:
        print(f)

    return {
        'dns': dns_data,
        'web': tech_data,
        'nmap_raw': nmap_output,
        'findings': findings,
        'dirb_found_pages': dirb_pages
    }