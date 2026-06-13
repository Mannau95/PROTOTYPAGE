import json
import csv
import random
from datetime import datetime, timedelta
import re

#Génération de transaction aléatoire
canaux = ["mobile", "agence", "ATM", "web"]
statuts = ["ok", "refusé", "suspect", "en attente"]

def generer_numero_benin():
    """Génère un numéro de mobile Bénin valide aléatoire."""
    # Indicatif : +229, 229 ou 00229
    indicatif = random.choice(["+229", "229", "00229"])
    # Deux premiers chiffres après indicatif : 01
    debut = "01"
    # Troisième chiffre : 9, 6, 5, 4, 2
    troisieme = random.choice(["9", "6", "5", "4", "2"])
    # 7 chiffres restants
    reste = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    numero = f"{indicatif} {debut} {troisieme}{reste}"  # avec espaces
    return numero

def generer_transactions(nombre=100):

    transactions = []
    maintenant = datetime.now()
    for i in range(1, nombre + 1 ):
        delta_jours = random.randint(0, 60)
        delta_secondes = random.randint(0, 86399)  # secondes dans une journée
        date_transaction = maintenant - timedelta(days=delta_jours, seconds=delta_secondes)
        date_iso = date_transaction.isoformat(sep='T', timespec='seconds')
        
        transaction = {
             "id": i,
             "montant": round(random.randint(1, 2000000) ), 
             "canal": random.choice(canaux),
             "statut": random.choice(statuts),
             "date": date_iso,
             "num_tel": generer_numero_benin () 
        }
        transactions.append(transaction)
    return transactions

def afficher_transactions(transactions):
    """Affiche toutes les transactions de manière lisible."""
    if not transactions:
        print("Aucune transaction à afficher.")
        return
    print("\n--- Liste des transactions ---")
    print(f"ID | Montant | Canal   | Statut   | Date                 | Numéro de téléphone")
    for t in transactions:
        print(f"ID {t['id']:<3} | {t['montant']:>6.2f} FCFA| {t['canal']:<8} | {t['statut']:<8} | {t['date']:<19} | {t.get('num_tel', 'N/A')}")

def filtrer_par_canal(transactions, canal):
    """Retourne la liste des transactions dont le canal correspond."""
    return [t for t in transactions if t["canal"] == canal]

def filtrer_par_statut(transactions, statut):
    """Retourne la liste des transactions dont le statut correspond."""
    return [t for t in transactions if t["statut"] == statut]

def statistiques(transactions):
    """Affiche le nombre de transactions par statut et le montant total par canal."""
    # Comptage par statut
    stats_statut = {}
    for t in transactions:
        statut = t["statut"]
        stats_statut[statut] = stats_statut.get(statut, 0) + 1
    
    # Montants totaux par canal
    total_par_canal = {}
    for t in transactions:
        canal = t["canal"]
        total_par_canal[canal] = total_par_canal.get(canal, 0) + t["montant"]
    
    print("\n Statistiques")
    print("Nombre de transactions par statut :")
    for statut, nb in stats_statut.items():
        print(f"  {statut} : {nb}")
    print("Montant total par canal :")
    for canal, total in total_par_canal.items():
        print(f"  {canal} : {total:.2f} FCFA")
        
def ajouter_transaction(transactions, transaction):
    """
    Ajoute une transaction à la liste.
    """
    # Vérification de l'unicité de l'id
    for t in transactions:
        if t["id"] == transaction["id"]:
            raise ValueError(f"Une transaction avec l'id {transaction['id']} existe déjà.")
    transactions.append(transaction)
    
def sauvegarder_json(transactions, nom_fichier="transactions.json"):
    """Sauvegarde la liste des transactions dans un fichier JSON."""
    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=4, ensure_ascii=False)
    print(f"Données sauvegardées dans {nom_fichier}(JSON)")

def charger_depuis_json(nom_fichier="transactions.json"):
    """Charge une liste de transactions depuis un fichier JSON (si existant)."""
    try:
        with open(nom_fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    
def sauvegarder_csv(transactions, nom_fichier="transactions.csv"):
    """Sauvegarde la liste des transactions au format CSV."""
    if not transactions:
        print("Aucune transaction à sauvegarder.")
        return
    with open(nom_fichier, "w", newline="", encoding="utf-8") as f:
        # Les clés du premier dictionnaire servent d'en-têtes de colonnes
        fieldnames = transactions[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)
    print(f"Transactions sauvegardées dans {nom_fichier} (CSV)")
