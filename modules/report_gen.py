# modules/report_gen.py

import os
from datetime import datetime

def save_report(target, analysis_results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = target.replace(":", "_").replace("/", "_")
    filename = f"outputs/report_{safe_target}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"====== Rapport NetGhost ======\n")
        f.write(f"Date : {datetime.now()}\n")
        f.write(f"Cible : {target}\n")
        f.write("="*30 + "\n\n")

        # DNS
        f.write("[+] Analyse DNS\n")
        dns = analysis_results['dns']
        f.write(f"- Whois: {dns.get('whois')}\n")
        f.write(f"- Sous-domaines trouvés : {', '.join(dns.get('subdomains_found', [])) or 'Aucun'}\n")
        f.write("- Zone transfer :\n")
        for srv, result in dns.get('zone_transfer', {}).items():
            f.write(f"  * {srv}: {'Possible' if result else 'Échec'}\n")

        # WebTech
        f.write("\n[+] Technologies Web\n")
        web = analysis_results['web']
        if web:
            f.write(f"- CMS : {', '.join(web.get('cms', [])) or 'Non détecté'}\n")
            f.write(f"- Frameworks : {', '.join(web.get('frameworks', [])) or 'Non détecté'}\n")
            f.write(f"- Langages : {', '.join(web.get('languages', [])) or 'Non détecté'}\n")
            f.write(f"- Serveur : {web.get('server') or 'Inconnu'}\n")
            f.write(f"- X-Powered-By: {web.get('x_powered_by') or 'Non détecté'}\n")
        else:
            f.write("Aucune information détectée.\n")

        f.write("\n[+] Scan Réseau (Nmap)\n")
        nmap_data = analysis_results.get('nmap_raw', '')
        f.write(nmap_data or "Aucun résultat.\n")

        f.write("\n[+] Synthèse de l’analyse\n")
        findings = analysis_results.get('findings', [])
        if findings:
            for line in findings:
                f.write(f"- {line}\n")
        else:
            f.write("Aucune anomalie détectée.\n")

    print(f"\nRapport sauvegardé dans : {filename}")
