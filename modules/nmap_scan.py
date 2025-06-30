import subprocess
import os
from datetime import datetime

def run(target, scan_args):
    try:
        print(f"Lancement de Nmap sur {target} avec options : {' '.join(scan_args)}")
        cmd = ["nmap", "-Pn"] + scan_args + [target]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        output = result.stdout

        os.makedirs("outputs", exist_ok=True)

        safe_target = target.replace(":", "_").replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/nmap_{safe_target}_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)

        print(f"Résultat Nmap sauvegardé dans {filename}")
        return output

    except Exception as e:
        print(f"Erreur pendant le scan Nmap : {e}")
        return ""
