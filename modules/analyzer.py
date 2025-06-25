# analyzer.py

from modules import dns_enum, webtech_detect, nmap_scan

def analyze_target(target, scan_args):
    print(f"\n[+] Lancement de l'analyse complète pour : {target}")
    findings = []

    # 1. DNS Enumeration
    print("[DNS] Analyse DNS...")
    dns_data = dns_enum.run(target)

    if any(dns_data['zone_transfer'].values()):
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

    # 2. Web Technologies
    print("[WEB] Détection des technologies web...")
    url = f"http://{target}"
    tech_data = webtech_detect.detect_technologies(url)

    if tech_data:
        if tech_data['cms']:
            findings.append(f"[+] CMS détecté : {', '.join(tech_data['cms'])}")
        if tech_data['frameworks']:
            findings.append(f"[*] Frameworks : {', '.join(tech_data['frameworks'])}")
        if tech_data['languages']:
            findings.append(f"[*] Langages backend : {', '.join(tech_data['languages'])}")
        if tech_data['server']:
            findings.append(f"[*] Serveur web : {tech_data['server']}")
        if tech_data['x_powered_by']:
            findings.append(f"[*] X-Powered-By : {tech_data['x_powered_by']}")

    # 3. Nmap Scan
    print("[NMAP] Scan réseau avec Nmap...")
    nmap_output = nmap_scan.run(target, scan_args)

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

    print("\n========== Synthèse de l'analyse ==========")
    for f in findings:
        print(f)

    return {
        'dns': dns_data,
        'web': tech_data,
        'nmap_raw': nmap_output,
        'findings': findings
    }
