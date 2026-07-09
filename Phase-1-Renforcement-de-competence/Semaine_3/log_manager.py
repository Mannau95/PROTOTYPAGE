
#  Gestion complète des logs transactionnels


import argparse
import json
import random
import sys
import time
import uuid
from datetime import datetime, timedelta
from collections import defaultdict

# ----------------------------------------------------------------------
# 1. Fonction de génération d'un log (reprise de generer_log.py)
# ----------------------------------------------------------------------

CANAUX = ["mobile", "en ligne", "ATM", "agence", "USSD"]
POIDS_CANAUX = [0.4, 0.3, 0.15, 0.1, 0.05]
STATUTS = ["ok", "refusé", "erreur", "suspect"]
POIDS_STATUTS = [0.9, 0.05, 0.03, 0.02]
CODE_REPONSE = {"ok": "00", "refusé": "05", "erreur": "99", "suspect": "44"}

def generer_timestamp(anomalie=False):
    maintenant = datetime.now()
    jours = random.randint(0, 7)
    jour = maintenant - timedelta(days=jours)
    if anomalie:
        heure = random.choice([0,1,2,3,4,5,22,23])
    else:
        if random.random() < 0.8:
            heure = random.randint(8, 17)
        else:
            heure = random.choice(list(range(0,8)) + list(range(18,24)))
    minute = random.randint(0, 59)
    seconde = random.randint(0, 59)
    return datetime(jour.year, jour.month, jour.day, heure, minute, seconde)

def generer_montant(anomalie=False):
    if anomalie:
        return random.randint(500000, 5000000)
    else:
        if random.random() < 0.8:
            return random.randint(100, 100000)
        else:
            return random.randint(100000, 5000000)

def generer_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

def generer_numero_benin(valide=True):
    if valide:
        indicatif = random.choice(["+229", "229"])
        troisieme = random.choice(["9", "5"])
        reste = ''.join([str(random.randint(0,9)) for _ in range(6)])
        return f"{indicatif} 01 {troisieme}{reste[:1]} {reste[1:3]} {reste[3:5]} {reste[5:]}"
    else:
        return f"{random.randint(100,999)} {random.randint(10,99)} {random.randint(100000,999999)}"

def generer_log(anomalie=False):
    canal = random.choices(CANAUX, weights=POIDS_CANAUX, k=1)[0]
    if anomalie:
        statut = random.choices(["suspect", "erreur", "refusé", "ok"], weights=[0.4, 0.3, 0.2, 0.1], k=1)[0]
        montant = generer_montant(anomalie=True)
        num_tel = generer_numero_benin(valide=False)
        timestamp = generer_timestamp(anomalie=True)
    else:
        statut = random.choices(STATUTS, weights=POIDS_STATUTS, k=1)[0]
        montant = generer_montant(anomalie=False)
        num_tel = generer_numero_benin(valide=True)
        timestamp = generer_timestamp(anomalie=False)
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

# ----------------------------------------------------------------------
# 2. Fonctions de génération massive
# ----------------------------------------------------------------------

def generer_logs(n, prob_anomalie=0.05):
    logs = []
    for _ in range(n):
        est_anormal = random.random() < prob_anomalie
        logs.append(generer_log(anomalie=est_anormal))
    return logs

def sauvegarder_jsonl(logs, fichier):
    with open(fichier, "w", encoding="utf-8") as f:
        for log in logs:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")
    print(f"{len(logs)} logs sauvegardés dans {fichier}", file=sys.stderr)

# ----------------------------------------------------------------------
# 3. Fonctions de simulation de flux
# ----------------------------------------------------------------------

def simuler_depuis_fichier(fichier, delai):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if ligne:
                    print(ligne, flush=True)
                    time.sleep(delai)
    except FileNotFoundError:
        print(f"Fichier {fichier} introuvable.", file=sys.stderr)
        sys.exit(1)

def simuler_en_continu(delai, prob_anomalie=0.05):
    while True:
        est_anormal = random.random() < prob_anomalie
        log = generer_log(anomalie=est_anormal)
        print(json.dumps(log, ensure_ascii=False), flush=True)
        time.sleep(delai)

# ----------------------------------------------------------------------
# 4. Fonctions de parsing et statistiques
# ----------------------------------------------------------------------

def parser_flux():
    stats = {
        "total": 0,
        "par_statut": defaultdict(int),
        "montant_par_canal": defaultdict(float),
        "anomalies": 0,
        "erreurs_parse": 0
    }
    try:
        for ligne in sys.stdin:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                log = json.loads(ligne)
                stats["total"] += 1
                stats["par_statut"][log.get("statut", "inconnu")] += 1
                canal = log.get("canal", "inconnu")
                montant = log.get("montant", 0)
                stats["montant_par_canal"][canal] += montant
                if (log.get("statut") == "suspect" or
                    log.get("montant", 0) > 1000000 or
                    "229" not in log.get("num_tel", "")):
                    stats["anomalies"] += 1
            except json.JSONDecodeError:
                stats["erreurs_parse"] += 1
    except KeyboardInterrupt:
        pass

    # Affichage du résumé (sur stderr)
    print("\n=== RÉSUMÉ DU FLUX ===", file=sys.stderr)
    print(f"Total transactions lues : {stats['total']}", file=sys.stderr)
    print(f"Erreurs de parsing : {stats['erreurs_parse']}", file=sys.stderr)
    print("\nRépartition par statut :", file=sys.stderr)
    for statut, nb in sorted(stats["par_statut"].items()):
        print(f"  {statut}: {nb}", file=sys.stderr)
    print("\nMontant total par canal :", file=sys.stderr)
    for canal, montant in sorted(stats["montant_par_canal"].items()):
        print(f"  {canal}: {montant:,.0f} FCFA", file=sys.stderr)
    print(f"\nAnomalies détectées : {stats['anomalies']}", file=sys.stderr)

# ----------------------------------------------------------------------
# 5. Interface en ligne de commande (sous-commandes)
# ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Gestion des logs transactionnels (génération, simulation, parsing)"
    )
    subparsers = parser.add_subparsers(dest="commande", required=True, help="Sous-commande")

    # --- Sous-commande generate ---
    gen_parser = subparsers.add_parser("generate", help="Générer des logs")
    gen_parser.add_argument("-n", "--nombre", type=int, default=1000,
                            help="Nombre de logs (défaut: 1000)")
    gen_parser.add_argument("-p", "--prob-anomalie", type=float, default=0.05,
                            help="Probabilité d'anomalie (défaut: 0.05)")
    gen_parser.add_argument("-o", "--output", default="transactions.jsonl",
                            help="Fichier de sortie (défaut: transactions.jsonl)")

    # --- Sous-commande simulate ---
    sim_parser = subparsers.add_parser("simulate", help="Simuler un flux de logs")
    sim_parser.add_argument("-f", "--fichier", default="transactions.jsonl",
                            help="Fichier JSONL à lire (défaut: transactions.jsonl)")
    sim_parser.add_argument("-d", "--delai", type=float, default=0.2,
                            help="Délai entre chaque log en secondes (défaut: 0.2)")
    sim_parser.add_argument("--infini", action="store_true",
                            help="Génération continue (ignore --fichier)")

    # --- Sous-commande parse ---
    parse_parser = subparsers.add_parser("parse", help="Parser les logs depuis stdin")
    parse_parser.add_argument("--fichier", help="(optionnel) lire depuis un fichier au lieu de stdin")

    args = parser.parse_args()

    if args.commande == "generate":
        logs = generer_logs(args.nombre, args.prob_anomalie)
        sauvegarder_jsonl(logs, args.output)

    elif args.commande == "simulate":
        if args.infini:
            simuler_en_continu(args.delai)
        else:
            simuler_depuis_fichier(args.fichier, args.delai)

    elif args.commande == "parse":
        if args.fichier:
            # Rediriger le contenu du fichier vers stdin du parser
            with open(args.fichier, "r", encoding="utf-8") as f:
                sys.stdin = f
                parser_flux()
        else:
            parser_flux()

if __name__ == "__main__":
    main()