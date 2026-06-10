def filtrer_par_canal(transactions, canal):
    """Retourne les transactions du canal donné."""
    return [t for t in transactions if t["canal"] == canal]

def ajouter_transaction(liste, transaction):
    """Ajoute une transaction si l'id n'existe pas déjà."""
    for t in liste:
        if t["id"] == transaction["id"]:
            raise ValueError(f"ID {transaction['id']} déjà présent.")
    liste.append(transaction)

def compter_par_statut(transactions):
    """Retourne un dict {statut: nombre}."""
    compteur = {}
    for t in transactions:
        statut = t["statut"]
        compteur[statut] = compteur.get(statut, 0) + 1
    return compteur