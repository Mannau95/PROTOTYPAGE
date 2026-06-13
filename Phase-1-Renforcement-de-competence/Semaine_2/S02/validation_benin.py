import re

def valider_numero_benin(num):
    """
    Valide un numéro de mobile Bénin.
    Formats acceptés :
        +229 01 9X XXXXXX
        +229 01 5X XXXXXX
        229 01 9X XXXXXX
        229 01 5X XXXXXX
    Les espaces sont optionnels.
    """
    pattern = r'^(?:\+229|229)\s*01\s*[59]\d{6}$'
    return bool(re.match(pattern, num))

def extraire_clef_valeur(log, clef):
    """
    Extrait la valeur d'une clé dans une chaîne "clef=valeur" séparée par des espaces.
    Exemple : log = "id=12345 timestamp=2026-06-08T14:23:05 montant=50000"
    extraire_clef_valeur(log, "montant") -> "50000"
    """
    pattern = rf'{re.escape(clef)}=([^\s]+)'
    match = re.search(pattern, log)
    return match.group(1) if match else None

# Test intégré
if __name__ == "__main__":
    # Test validation
    tests = [
        "+229 01 97 12 34 56",
        "229 01 98 76 54 32",
        "+229 01 55 55 55 55",
        "2290155123456",      # sans espaces
        "+229 01 99 99 99 99",
        "00229 01 97 12 34 56",  # invalide
        "229 02 97 12 34 56"      # invalide (pas 01)
    ]
    for t in tests:
        print(f"{t:30} -> {valider_numero_benin(t)}")
    
    # Test extraction
    log = "id=12345 timestamp=2026-06-08T14:23:05 montant=50000 canal=mobile"
    print("\nExtraction :")
    print(f"id : {extraire_clef_valeur(log, 'id')}")
    print(f"montant : {extraire_clef_valeur(log, 'montant')}")
    print(f"canal : {extraire_clef_valeur(log, 'canal')}")
    print(f"inexistant : {extraire_clef_valeur(log, 'toto')}")