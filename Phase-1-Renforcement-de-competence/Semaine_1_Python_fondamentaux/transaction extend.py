nouvelles_transactions = [
    {"id": 1, "montant": 4550, "canal": "web", "statut": "echec"},
    {"id": 2, "montant": 21000, "canal": "web", "statut": "ok"},
    {"id": 3, "montant": 3200, "canal": "mobile", "statut": "ok"},
    {"id": 4, "montant": 92030, "canal": "mobile", "statut": "en_attente"},
    {"id": 5, "montant": 2030, "canal": "mobile", "statut": "ok"},
    {"id": 6, "montant": 330, "canal": "web", "statut": "ok"},
    {"id": 7, "montant": 32030, "canal": "mobile", "statut": "ok"},
    {"id": 8, "montant": 320, "canal": "web", "statut": "en_attente"},
    {"id": 9, "montant": 562030, "canal": "web", "statut": "en_attente"},
    {"id":10, "montant": 42030, "canal": "mobile", "statut": "ok"}
]

# Affichage complet 
print(" Liste complète des transactions")
for t in nouvelles_transactions:
    print(f"ID {t['id']} : {t['montant']}FCFA, canal={t['canal']}, statut={t['statut']}")
print()

# Fonction de filtrage
def filtrer_par_statut(transactions, statut):
    """Retourne les transactions dont le statut correspond."""
    return [t for t in transactions if t["statut"] == statut]

# afficher les transactions avec statut "ok"
print("Transactions avec statut 'ok' ")
ok_transactions = filtrer_par_statut(nouvelles_transactions, "ok")
for t in ok_transactions:
    print(f"ID {t['id']} : {t['montant']}FCFA via {t['canal']}")
print()
# afficher les transactions avec statut "en_attente"
print("Transactions avec statut 'en_attente' ")
ok_transaction = filtrer_par_statut(nouvelles_transactions, "en_attente")
for t in ok_transaction:
    print(f"ID {t['id']} : {t['montant']}FCFA via {t['canal']}")
print()