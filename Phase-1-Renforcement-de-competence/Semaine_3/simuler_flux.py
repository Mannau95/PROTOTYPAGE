# simuler_flux.py
import argparse
import json
import time
import sys
from generer_log import generer_log

def simuler_fichier(fichier, delai):
    """Lit un fichier JSONL et envoie chaque ligne avec un délai."""
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if ligne:
                    #  timestamp de réception simulé
                    print(ligne, flush=True)
                    time.sleep(delai)
    except FileNotFoundError:
        print(f"Fichier {fichier} introuvable.", file=sys.stderr)
        sys.exit(1)

def simuler_live(delai):
    """Génère des logs en continu et les envoie sur stdout."""
    while True:
        log = generer_log(anomalie=True)  
        print(json.dumps(log, ensure_ascii=False), flush=True)
        time.sleep(delai)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simule un flux de logs")
    parser.add_argument("--fichier", "-f", default="transactions.jsonl", help="Fichier JSONL à lire")
    parser.add_argument("--delai", "-d", type=float, default=0.2, help="Délai entre chaque log (secondes)")
    parser.add_argument("--infini", action="store_true", help="Génération continue de nouveaux logs (ignore --fichier)")
    args = parser.parse_args()
    
    if args.infini:
        simuler_live(args.delai)
    else:
        simuler_fichier(args.fichier, args.delai)