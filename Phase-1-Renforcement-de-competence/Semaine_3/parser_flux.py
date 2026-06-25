# parser_flux.py
import sys
import json
from collections import defaultdict

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
                # Détection d'anomalies (exemple: montant > 1 000 000, statut suspect, numéro invalide)
                if (log.get("statut") == "suspect" or 
                    log.get("montant", 0) > 1000000 or
                    "229" not in log.get("num_tel", "")):
                    stats["anomalies"] += 1
            except json.JSONDecodeError:
                stats["erreurs_parse"] += 1
    except KeyboardInterrupt:
        # Affichage du résumé même en cas d'interruption
        pass
    
    # Affichage du résumé
    print("\n=== RÉSUMÉ DU FLUX ===", file=sys.stderr)
    print(f"Total transactions lues : {stats['total']}", file=sys.stderr)
    print(f"Erreurs de parsing : {stats['erreurs_parse']}", file=sys.stderr)
    print("\nRépartition par statut :", file=sys.stderr)
    for statut, nb in stats["par_statut"].items():
        print(f"  {statut}: {nb}", file=sys.stderr)
    print("\nMontant total par canal :", file=sys.stderr)
    for canal, montant in stats["montant_par_canal"].items():
        print(f"  {canal}: {montant:,.0f} FCFA", file=sys.stderr)
    print(f"\nAnomalies détectées : {stats['anomalies']}", file=sys.stderr)

if __name__ == "__main__":
    parser_flux()