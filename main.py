# main.py

import sys
from modules.scan_profiles import get_scan_type
from modules.analyzer import analyze_target
from modules.report_gen import save_report

def main():
    target = input("Entrez la cible à analyser (IP ou domaine) : ").strip()
    if not target:
        print("Erreur : cible vide.")
        sys.exit(1)

    print("\nChoisissez le type de scan Nmap :")
    print("1) Scan SYN (-sS), version (-sV) et OS (-O)")
    print("2) Scan complet ports (-p-) et version (-sV)")
    print("3) Scan rapide (-F)")
    print("4) Scan agressif (-A)")
    print("5) Options personnalisées")
    scan_choice = input("Votre choix (1-5) : ").strip()

    scan_args = get_scan_type(scan_choice)

    results = analyze_target(target, scan_args)


    save_report(target, results)

    print("\nAnalyse terminée !")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompu par l'utilisateur.")
        sys.exit(0)
