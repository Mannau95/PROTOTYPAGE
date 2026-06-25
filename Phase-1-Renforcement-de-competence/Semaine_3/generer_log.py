# generer_log.py (module pour générer un log unique)
import random
import uuid
from datetime import datetime, timedelta, time


CANAUX = ["mobile", "en ligne", "ATM", "agence", "USSD"]
POIDS_CANAUX = [0.4, 0.3, 0.15, 0.1, 0.05]
STATUTS = ["ok", "refusé", "erreur", "suspect"]
POIDS_STATUTS = [0.9, 0.05, 0.03, 0.02]
CODE_REPONSE = {"ok": "00", "refusé": "05", "erreur": "99", "suspect": "44"}

def generer_timestamp():
    """Génère un timestamp dans les 7 derniers jours avec préférence pour les heures ouvrées."""
    maintenant = datetime.now()
    jours = random.randint(0, 7)
    jour = maintenant - timedelta(days=jours)
    # 70% de chances d'être en heures ouvrées (8h-18h), 30% hors
    if random.random() < 0.7:
        heure = random.randint(8, 17)
        minute = random.randint(0, 59)
        seconde = random.randint(0, 59)
    else:
        heure = random.choice(list(range(0,8)) + list(range(18,24)))
        minute = random.randint(0, 59)
        seconde = random.randint(0, 59)
    return datetime(jour.year, jour.month, jour.day, heure, minute, seconde)

def generer_montant():
    """75% de petits montants, 25% de grands."""
    if random.random() < 0.75:
        return random.randint(1, 100000)
    else:
        return random.randint(100000, 5000000)

def generer_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

def generer_numero_benin(valide=True):
    """Génère un numéro béninois valide ou invalide."""
    if valide:
        indicatif = random.choice(["+229", "229", "00229"])
        debut = "01"
        troisieme = random.choice(["9", "5", "6", "4", "2"])
        reste = ''.join([str(random.randint(0,9)) for _ in range(7)])
        return f"{indicatif} {debut} {troisieme}{reste[:1]} {reste[1:3]} {reste[3:5]} {reste[5:]}"
    else:
        # invalide : mauvais format
        return f"{random.randint(100,999)} {random.randint(10,99)} {random.randint(100000,999999)}"

def generer_log(anomalie=False):
    """
    Génère un log transactionnel.
    Si anomalie=True, on force des caractéristiques suspectes.
    """
    canal = random.choices(CANAUX, weights=POIDS_CANAUX, k=1)[0]
    if anomalie:
        # On modifie les probabilités pour générer des anomalies
        statut = random.choices(["suspect", "erreur", "refusé", "ok"], weights=[0.3, 0.3, 0.3, 0.1], k=1)[0]
        montant = random.randint(500000, 5000000)  # montant élevé
        num_tel = generer_numero_benin(valide=False)  # numéro invalide
        # heure nocturne
        timestamp = generer_timestamp()
        timestamp = timestamp.replace(hour=random.choice([2,3,4,5,22,23,0,1]))
    else:
        statut = random.choices(STATUTS, weights=POIDS_STATUTS, k=1)[0]
        montant = generer_montant()
        num_tel = generer_numero_benin(valide=True)
        timestamp = generer_timestamp()
    
    return {
        "id": str(uuid.uuid4()),
        "timestamp": timestamp.isoformat(),
        "montant": montant,
        "canal": canal,
        "statut": statut,
        "code_reponse": CODE_REPONSE[statut],
        "id_client": random.randint(1000, 99999),
        "num_tel": num_tel,
        "ip_source": generer_ip(),
        "pays": "BJ",
        "duree_session_ms": random.randint(1000, 60000),
        "empreinte_appareil": f"device_{random.randint(1000,9999)}",
        "geolocalisation": {
            "lat": round(random.uniform(6.2, 12.5), 4),
            "lon": round(random.uniform(0.8, 3.8), 4)
        },
        "code_marchand": random.randint(1000, 9999) if random.random() < 0.3 else None
    }

