import random

# Génération de 20 transactions aléatoires
canaux = ["mobile", "agence", "ATM", "en ligne"]
statuts = ["ok", "refusé", "suspect"]

transactions = []
for i in range(1, 21):
    transaction = {
        "id": i,
        "montant": random.randint(10, 2000000) , 
        "canal": random.choice(canaux),
        "statut": random.choice(statuts)
    }
    transactions.append(transaction)

# Affichage des 5 premières pour vérifier
print(" Toutes les transactions")
for t in transactions[:20]:
    print(t)
print()  
    
print("5 premières transactions")
for t in transactions[:5]:
    print(t)

# 2. Fonctions sous forme de one-liners (compréhensions)

# transactions suspectes
transactions_suspectes = [t for t in transactions if t["statut"] == "suspect"]

# montants des transactions suspectes
montants_suspects = [t["montant"] for t in transactions_suspectes]

# somme des montants suspects
somme_suspects = sum(t["montant"] for t in transactions_suspectes)  # générateur

# transaction avec le montant le plus élevé
# key=lambda x: x['montant'] signifie : extraire la valeur de la clé 'montant' pour chaque dict x
transaction_la_plus_elevee = max(transactions, key=lambda x: x["montant"])

# Affichage des résultats
print("\n=== Transactions suspectes ===")
for t in transactions_suspectes:
    print(f"ID {t['id']} : {t['montant']}FCFA via {t['canal']}")

print(f"\nMontants suspects : {montants_suspects}FCFA")
print(f"Somme des montants suspects : {somme_suspects:.2f} FCFA")
print(f"Transaction la plus élevée : ID {transaction_la_plus_elevee['id']} - {transaction_la_plus_elevee['montant']}FCFA")

# 3. Fonction grouper_par_canal
def grouper_par_canal(transactions):
    resultat = {}
    for t in transactions:
        canal = t["canal"]
        if canal not in resultat:
            resultat[canal] = []
        resultat[canal].append(t)
    return resultat

# Test du groupement
groupes = grouper_par_canal(transactions)
print("\nTransactions par canal")
for canal, liste in groupes.items():
    print(f"{canal} : {len(liste)} transaction(s)")
    for t in liste[:3]:  # affiche les 3 premières de chaque canal
        print(f"  - ID {t['id']} : {t['montant']}FCFA, statut {t['statut']}")

