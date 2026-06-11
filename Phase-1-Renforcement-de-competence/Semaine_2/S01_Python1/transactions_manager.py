from outils_transactions import (
    generer_transactions,
    afficher_transactions,
    filtrer_par_canal,
    filtrer_par_statut,
    statistiques,
    ajouter_transaction,
    sauvegarder_json,
    sauvegarder_csv,
    charger_depuis_json
)
def saisir_transaction(transactions_existantes):
    """Demande à l'utilisateur les données d'une nouvelle transaction."""
    print("\n--- Ajout d'une nouvelle transaction ---")
    # Trouver le prochain id disponible
    ids_existants = [t["id"] for t in transactions_existantes]
    nouvel_id = max(ids_existants) + 1 if ids_existants else 1
    
    montant = float(input("Montant (ex: 1000) : "))
    # Validation simple du canal
    while True:
        canal = input("Canal (mobile/agence/ATM/en ligne) : ").strip().lower()
        if canal in ["mobile", "agence", "atm", "web"]:
            if canal == "atm":
                canal = "ATM"  
            break
        print("Canal invalide. Choisir parmi : mobile, agence, ATM, en ligne")
    
    statut = input("Statut (ok/refusé/suspect/en attente) : ").strip().lower()
    while statut not in ["ok", "refusé", "suspect", "en attente"]:
        print("Statut invalide. Choisir parmi : ok, refusé, suspect, en attente4")
        statut = input("Statut : ").strip().lower()
    
    from datetime import datetime
    date_iso = datetime.now().isoformat(sep='T', timespec='seconds')
    
    nouvelle = {
        "id": nouvel_id,
        "montant": round(montant, 2),
        "canal": canal,
        "statut": statut,
        "date": date_iso
    }
    return nouvelle
def menu():
    """Affiche le menu et gère la boucle principale."""
    # Chargement éventuel d'une sauvegarde existante
    transactions = charger_depuis_json()
    if transactions is None:
        print("Aucune sauvegarde trouvée. Génération de 100 transactions aléatoires.")
        transactions = generer_transactions(100)
    else:
        print(f"{len(transactions)} transactions chargées depuis le fichier.")
    
    while True:
        print("\n" + "=" * 100)
        print("GESTIONNAIRE DE TRANSACTIONS")
        print("1. Afficher toutes les transactions")
        print("2. Filtrer par canal")
        print("3. Filtrer par statut")
        print("4. Afficher les statistiques")
        print("5. Ajouter une nouvelle transaction")
        print("6. Sauvegarder en CSV")
        print("7. Sauvegarder en json")
        print("8. Quitter")
        choix = input("Votre choix (1-8) : ").strip()
        
        if choix == "1":
            afficher_transactions(transactions)
        elif choix == "2":
            canal = input("Quel canal ? (mobile/agence/ATM/en ligne) : ").strip().lower()
            if canal == "atm":
                canal = "ATM"
            filtrees = filtrer_par_canal(transactions, canal)
            afficher_transactions(filtrees)
        elif choix == "3":
            statut = input("Quel statut ? (ok/refusé/suspect/en attente) : ").strip().lower()
            filtrees = filtrer_par_statut(transactions, statut)
            afficher_transactions(filtrees)
        elif choix == "4":
            statistiques(transactions)
        elif choix == "5":
            try:
                nouvelle = saisir_transaction(transactions)
                ajouter_transaction(transactions, nouvelle)
                print("Transaction ajoutée avec succès !")
            except ValueError as e:
                print(f"Erreur : {e}")
            except Exception as e:
                print(f"Erreur inattendue : {e}")
        elif choix == "6":
            sauvegarder_csv(transactions)
        elif choix == "7":
            sauvegarder_json(transactions)
        elif choix == "8":
            print("Au revoir !")
            break
        else:
            print("Choix invalide, veuillez entrer un nombre entre 1 et 6.")

if __name__ == "__main__":
    menu()