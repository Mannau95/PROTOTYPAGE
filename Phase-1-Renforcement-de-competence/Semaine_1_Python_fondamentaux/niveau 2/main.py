import mes_outils   

# Données initiales
transactions = [
    {"id": 1, "montant": 4550, "canal": "web", "statut": "echec"},
    {"id": 2, "montant": 21000, "canal": "web", "statut": "ok"},
    {"id": 3, "montant": 3200, "canal": "mobile", "statut": "ok"},
    {"id": 4, "montant": 92030, "canal": "mobile", "statut": "en_attente"},
    {"id": 5, "montant": 2030, "canal": "mobile", "statut": "ok"},
    {"id": 6, "montant": 330, "canal": "web", "statut": "ok"},
    {"id": 7, "montant": 32030, "canal": "mobile", "statut": "ok"},
    {"id": 8, "montant": 320, "canal": "web", "statut": "en_attente"},
    {"id": 9, "montant": 562030, "canal": "web", "statut": "en_attente"},
    {"id":10, "montant": 42030, "canal": "mobile", "statut": "ok"},
    {"id":11, "montant": 42000, "canal": "mobile", "statut": "ok"},
    {"id":12, "montant": 20000, "canal": "web", "statut": "echec"},
    {"id":13, "montant": 675500, "canal": "mobile", "statut": "en_attente"},
    {"id":14, "montant": 45600, "canal": "web", "statut": "echec"},
    {"id":15, "montant": 95345200, "canal": "mobile", "statut": "echec"},
    {"id":16, "montant": 23400, "canal": "web", "statut": "en_attente"},
    {"id":17, "montant": 420090, "canal": "web", "statut": "ok"},
    {"id":18, "montant": 420540, "canal": "mobile", "statut": "ok"},
    {"id":19, "montant": 42900, "canal": "mobile", "statut": "echec"},
    {"id":20, "montant": 420, "canal": "mobile", "statut": "ok"}
]

# Test de compréhension de liste via la fonction
print("Filtrage canal 'mobile' :")
mobile = mes_outils.filtrer_par_canal(transactions, "mobile")
for t in mobile:
    print(t)
print()   
 
print("Filtrage canal 'web' :")
web = mes_outils.filtrer_par_canal(transactions, "web")
for t in web:
    print(t)
print()

# Test d'ajout
nouvelle = {"id": 21, "montant": 45050, "canal": "web", "statut": "echec"}
try:
    mes_outils.ajouter_transaction(transactions, nouvelle)
    print("\nTransaction ajoutée avec succès.")
except ValueError as e:
    print("Erreur :", e)

# Test d'ajout avec id existant
duplicat = {"id": 1, "montant": 99.99, "canal": "mobile", "statut": "ok"}
try:
    mes_outils.ajouter_transaction(transactions, duplicat)
except ValueError as e:
    print("\nErreur attendue :", e)

# Comptage par statut
print("\nComptage par statut :")
stats = mes_outils.compter_par_statut(transactions)
print(stats)