# Liste de montants de transactions
montants = [500, 1350, 850, 5000, 3057, 1740,63758,96474,5341,82503,143748,234]

print("Affichage des transactions") 
for i, montant in enumerate(montants, start=1):
    print(f"Transaction {i}: {montant} FCFA")

# Dictionnaire représentant une transaction
transaction_type = {
    "id": 1,
    "montant": 1350,
    "canal": "mobile",
    "statut": "ok"
}
print("\nExemple de dictionnire de transaction:", transaction_type)

# Création de liste de  dictionnaires 
transactions = [
    {"id": 1, "montant": 500, "canal": "mobile", "statut": "ok"},
    {"id": 2, "montant": 1350, "canal": "web", "statut": "en_attente"},
    {"id": 3, "montant": 850, "canal": "mobile", "statut": "ok"},
    {"id": 4, "montant": 5000, "canal": "mobile", "statut": "ok"},
    {"id": 5, "montant": 3057, "canal": "mobile", "statut": "ok"},
    {"id": 6, "montant": 1740, "canal": "mobile", "statut": "en_attente"},
    {"id": 7, "montant": 96474, "canal": "web", "statut": "ok"},
    {"id": 8, "montant": 5341, "canal": "web", "statut": "ok"},
    {"id": 9, "montant": 82503, "canal": "web", "statut": "en_attente"},
    {"id": 10, "montant": 63758, "canal": "mobile", "statut": "ok"}

]
print("\nNouvelles transactions:", transactions)

# Fonction filtrer_par_canal
def filtrer_par_canal(transactions, canal):
    """
    Retourne la liste des transactions dont le canal correspond à `canal`.
    """
    return [t for t in transactions if t["canal"] == canal]
print("\n Test du filtre ")
print("\n=== Test du filtre ===")
canal_recherche = "mobile"
resultat = filtrer_par_canal(transactions, canal_recherche)
print(f"Transactions du canal '{canal_recherche}' :")
for t in resultat:
    print(t)

canal_recherche2 = "web"
resultat2 = filtrer_par_canal(transactions, canal_recherche2)
print(f"\nTransactions du canal '{canal_recherche2}' :")
for t in resultat2:
    print(t)