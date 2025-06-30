def get_scan_type(choice):
    if choice == "1":
        return ["-Pn", "-sT", "-p-", "-sV"]
    elif choice == "2":
        return ["-p-", "-sV"]
    elif choice == "3":
        return ["-F"]
    elif choice == "4":
        return ["-A"]
    elif choice == "5":
        custom = input("Entrez les options personnalisées pour nmap (ex: -sS -p 80): ")
        return custom.split()
    else:
        print("Choix invalide, scan rapide par défaut (-F).")
        return ["-F"]