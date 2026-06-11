import csv
import json
import os
from datetime import datetime, date, time, timedelta

def charger_csv(fichier):
    """Lit CSV et convertit la colonne 'date' en datetime."""
    transactions = []
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            attendu = {"id", "montant", "canal", "statut", "date"}
            if not attendu.issubset(reader.fieldnames):
                raise ValueError(f"Colonnes manquantes. Attendues : {attendu}")
            for ligne in reader:
                ligne["id"] = int(ligne["id"])
                ligne["montant"] = float(ligne["montant"])
                ligne["date"] = datetime.fromisoformat(ligne["date"])  # str -> datetime
                transactions.append(ligne)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV introuvable : {fichier}")
    except csv.Error as e:
        raise ValueError(f"Erreur CSV : {e}")
    return transactions

def charger_json(fichier):
    """Lit JSON et convertit la colonne 'date' en datetime."""
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Le JSON ne contient pas une liste.")
            for t in data:
                t["id"] = int(t["id"])
                t["montant"] = float(t["montant"])
                t["date"] = datetime.fromisoformat(t["date"])
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON introuvable : {fichier}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide : {e}")

def charger_transactions(fichier):
    """Détecte le format via extension et charge."""
    ext = os.path.splitext(fichier)[1].lower()
    if ext == ".csv":
        return charger_csv(fichier)
    elif ext == ".json":
        return charger_json(fichier)
    else:
        raise ValueError(f"Format non supporté : {ext}")

def filtrer_par_periode(transactions, debut, fin):
    """
    Retourne les transactions avec date entre debut et fin.
    debut, fin peuvent être str (ISO), datetime ou date.
    """
    # Convertir en datetime si nécessaire
    if isinstance(debut, str):
        debut = datetime.fromisoformat(debut)
    if isinstance(fin, str):
        fin = datetime.fromisoformat(fin)
    # Si c'est une date (sans heure), on prend toute la journée
    if isinstance(debut, date) and not isinstance(debut, datetime):
        debut = datetime.combine(debut, time.min)
    if isinstance(fin, date) and not isinstance(fin, datetime):
        fin = datetime.combine(fin, time.max)
    
    return [t for t in transactions if debut <= t["date"] <= fin]

def resume_quotidien(transactions):
    """
    Regroupe par jour (date) et retourne dict:
    { date: {"nb": int, "total": float} }
    """
    result = {}
    for t in transactions:
        jour = t["date"].date()  # datetime -> date
        if jour not in result:
            result[jour] = {"nb": 0, "total": 0.0}
        result[jour]["nb"] += 1
        result[jour]["total"] += t["montant"]
    return result

def afficher_resume(resume):
    """Affiche le résumé quotidien sous forme de tableau."""
    if not resume:
        print("Aucune transaction.")
        return
    print("\n--- Résumé quotidien ---")
    print(f"{'Date':<12} | {'Nb':>4} | {'Total (FCFA)':>10}")
    print("-" * 30)
    for jour, stats in sorted(resume.items()):
        print(f"{jour.isoformat():<12} | {stats['nb']:>4} | {stats['total']:>10.2f}")

# Exemple d'utilisation
if __name__ == "__main__":
    # Charger les fichiers générés précédemment
    for fichier in ["transactions.csv", "transactions.json"]:
        try:
            transactions = charger_transactions(fichier)
            print(f"\n{fichier} : {len(transactions)} transactions chargées (dates en datetime)")
            
            # Test du filtre sur les 7 derniers jours
            aujourd_hui = datetime.now().date()
            debut = aujourd_hui - timedelta(days=7)
            filtrees = filtrer_par_periode(transactions, debut, aujourd_hui)
            print(f"Transactions des 7 derniers jours : {len(filtrees)}")
            
            # Résumé quotidien
            resume = resume_quotidien(transactions)
            afficher_resume(resume)
            
        except Exception as e:
            print(f"Erreur avec {fichier} : {e}")