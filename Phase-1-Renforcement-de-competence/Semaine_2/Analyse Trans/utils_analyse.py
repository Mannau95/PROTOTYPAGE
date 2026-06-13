import csv
import json
import re
from datetime import datetime

def valider_numero_benin(num):
    """Valide un numéro de mobile Bénin : +229, 0029 ou 229, puis 01, puis 9,6,4,2ou 5, puis 7 chiffres."""
    if not isinstance(num, str):
        return False
    pattern = r'^(?:\+229|229|00229)\s*01\s*[24569]\d{7}$'
    return bool(re.match(pattern, num.strip()))

def charger_transactions_csv(fichier):
    """Lit un CSV, convertit la date en datetime, retourne une liste de dicts."""
    transactions = []
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['id'] = int(row['id'])
                row['montant'] = float(row['montant'])
                row['date'] = datetime.fromisoformat(row['date'])
                transactions.append(row)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier {fichier} introuvable.")
    except ValueError as e:
        raise ValueError(f"Erreur de conversion (date ou nombre) : {e}")
    return transactions

def resume_statistiques(transactions):
    """Retourne (nb_total, dict_montant_par_canal, dict_nb_par_statut, date_max)."""
    nb_total = len(transactions)
    montant_par_canal = {}
    nb_par_statut = {}
    date_max = None
    for t in transactions:
        canal = t['canal']
        montant_par_canal[canal] = montant_par_canal.get(canal, 0) + t['montant']
        statut = t['statut']
        nb_par_statut[statut] = nb_par_statut.get(statut, 0) + 1
        if date_max is None or t['date'] > date_max:
            date_max = t['date']
    return nb_total, montant_par_canal, nb_par_statut, date_max

def transactions_dernier_jour(transactions, date_max):
    """Filtre les transactions du même jour que date_max."""
    jour = date_max.date()
    return [t for t in transactions if t['date'].date() == jour]

def transactions_invalides(transactions):
    """Retourne la liste des transactions dont le numéro ne valide pas la regex."""
    return [t for t in transactions if not valider_numero_benin(t.get('num_tel', ''))]

def sauvegarder_json(data, fichier):
    """Sauvegarde une liste de dicts en JSON, en convertissant les datetime en string ISO."""
    def convert(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} non sérialisable")
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False, default=convert)