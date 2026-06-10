transactions = []

#  Ajout avec append() - une transaction à la fois
transactions.append({"id": 1, "montant": 1500, "canal": "mobile", "statut": "ok"})
transactions.append({"id": 2, "montant": 8999, "canal": "web", "statut": "en_attente"})
transactions.append({"id": 3, "montant": 3200, "canal": "mobile", "statut": "ok"})
transactions.append({"id": 4, "montant": 92030, "canal": "mobile", "statut": "en_attente"})
transactions.append({"id": 5, "montant": 2030, "canal": "mobile", "statut": "ok"})
transactions.append({"id": 6, "montant": 330, "canal": "web", "statut": "ok"})
transactions.append({"id": 7, "montant": 32030, "canal": "mobile", "statut": "ok"})
transactions.append({"id": 8, "montant": 320, "canal": "web", "statut": "en_attente"})
transactions.append({"id": 9, "montant": 562030, "canal": "web", "statut": "en_attente"})
transactions.append({"id":10, "montant": 42030, "canal": "mobile", "statut": "ok"})
 

# Affichage complet 
print(" Liste complète des transactions")
for t in transactions:
    print(f"ID {t['id']} : {t['montant']}FCFA, canal={t['canal']}, statut={t['statut']}")
print()

# Fonction de filtrage
def filtrer_par_statut(transactions, statut):
    """Retourne les transactions dont le statut correspond."""
    return [t for t in transactions if t["statut"] == statut]

# afficher les transactions avec statut "ok"
print("Transactions avec statut 'ok' ")
ok_transactions = filtrer_par_statut(transactions, "ok")
for t in ok_transactions:
    print(f"ID {t['id']} : {t['montant']}FCFA via {t['canal']}")
print()
# afficher les transactions avec statut "en_attente"
print("Transactions avec statut 'en_attente' ")
ok_transaction = filtrer_par_statut(transactions, "en_attente")
for t in ok_transaction:
    print(f"ID {t['id']} : {t['montant']}FCFA via {t['canal']}")
print()  
    
def filtrer_par_canal(transactions, canal):
    """Retourne les transactions dont le statut correspond."""
    return [t for t in transactions if t["canal"] == canal]

# afficher les transactions avec canal "mobile"
print("Transactions avec canal 'mobile' ")
canal_transactions = filtrer_par_canal(transactions, "mobile")
for t in canal_transactions:
    print(f"ID {t['id']} : {t['montant']}FCFA via {t['statut']}")
print()  

# afficher les transactions avec canal "web"
print("Transactions avec canal 'web' ")
canal_transaction = filtrer_par_canal(transactions, "web")
for t in canal_transaction:
    print(f"ID {t['id']} : {t['montant']}FCFA via {t['statut']}")
print()  