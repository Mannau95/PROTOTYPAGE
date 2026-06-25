
# generateur_logs.py

import random
import json
from generer_log import generer_log

# Constantes
NB_LOGS = 1000
NB_ANOMALIES = 80

def generer_logs(n=NB_LOGS, nb_anomalies=NB_ANOMALIES):
    """
    Génère une liste de n logs, avec exactement nb_anomalies marquées comme anomalies.
    """
    logs = []
    # Générer les logs normaux
    for _ in range(n - nb_anomalies):
        logs.append(generer_log(anomalie=False))
    # Générer les logs anormaux
    for _ in range(nb_anomalies):
        logs.append(generer_log(anomalie=True))
    # Mélanger pour répartir les anomalies
    random.shuffle(logs)
    return logs

def sauvegarder_jsonl(logs, fichier="transactions.jsonl"):
    """Sauvegarde les logs au format JSON Lines."""
    with open(fichier, "w", encoding="utf-8") as f:
        for log in logs:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")
    print(f"{len(logs)} logs sauvegardés dans {fichier}")


if __name__ == "__main__":
    logs = generer_logs()
    sauvegarder_jsonl(logs)