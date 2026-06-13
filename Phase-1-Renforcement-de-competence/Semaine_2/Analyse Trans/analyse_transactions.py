import sys
from utils_analyse import (
    charger_transactions_csv,
    resume_statistiques,
    transactions_dernier_jour,
    transactions_invalides,
    sauvegarder_json
)

def main():
    fichier = "transactions.csv"
    try:
        transactions = charger_transactions_csv(fichier)
    except FileNotFoundError as e:
        print(f"Erreur : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur de lecture : {e}")
        sys.exit(1)

    # Statistiques
    nb_total, montant_par_canal, nb_par_statut, date_max = resume_statistiques(transactions)

    print("=== RÉSUMÉ DES TRANSACTIONS ===\n")
    print(f"Nombre total de transactions : {nb_total}\n")

    print("Montant total par canal :")
    for canal, montant in sorted(montant_par_canal.items()):
        print(f"  {canal} : {montant:.2f} FCFA")

    print("\nNombre de transactions par statut :")
    for statut, nb in sorted(nb_par_statut.items()):
        print(f"  {statut} : {nb}")

    # Dernier jour
    dernier_jour = transactions_dernier_jour(transactions, date_max)
    print(f"\nTransactions du dernier jour ({date_max.date().isoformat()}) : {len(dernier_jour)}")

    # Numéros invalides
    invalides = transactions_invalides(transactions)
    print(f"\nTransactions avec numéro invalide : {len(invalides)}")
    if invalides:
        print("  ID | Numéro")
        for t in invalides:
            print(f"  {t['id']} - {t.get('num_tel', 'N/A')}")
        sauvegarder_json(invalides, "anomalies.json")
        print("\nAnomalies sauvegardées dans anomalies.json")
    else:
        print("  Aucun numéro invalide détecté.")

if __name__ == "__main__":
    main()