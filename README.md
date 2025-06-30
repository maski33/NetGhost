# NetGhost

**NetGhost** est un outil Python modulaire destiné à l'analyse de cibles réseau et web. Il centralise plusieurs techniques classiques de reconnaissance : scan de ports avec Nmap, détection de technologies, énumération DNS, et découverte de chemins avec une attaque de type *dirbusting*.

---

## Fonctionnalités

- 🔍 **Scan Nmap** personnalisable (SYN, full port, agressif, rapide, etc.)
- 🌐 **Détection des technologies web** (via analyse HTTP)
- 🌍 **Énumération DNS** (DNS standard, transfert de zone, WHOIS, sous-domaines)
- 🗂️ **Scan Dirb** (attaque par dictionnaire de chemins)
- 📝 **Génération automatique de rapports**

---

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/netghost.git
   cd netghost
   ```

2. **Installer les dépendances Python** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Assurez-vous que `nmap` est installé sur votre machine** :
   - Sous Debian/Ubuntu : `sudo apt install nmap`
   - Sous Windows : [Télécharger Nmap](https://nmap.org/download.html)

---

## Utilisation

Lancer le script principal :

```bash
python main.py
```

Puis suivez les instructions interactives pour :
- Entrer une cible (IP ou domaine)
- Choisir d'effectuer ou non un scan Nmap
- Lancer ou non l'analyse DNS
- Exécuter ou non un scan dirb
- Fournir une wordlist personnalisée pour le scan dirb
- Récupérer les en-têtes HTTP

---

## Structure du projet

```
NetGhost/
├── main.py
├── requirements.txt
├── outputs/
│   └── (rapports générés)
├── modules/
│   ├── analyzer.py
│   ├── dirb.py
│   ├── dns_enum.py
│   ├── nmap_scan.py
│   ├── report_gen.py
│   ├── scan_profile.py
│   └── webtech_detect.py
```

---


