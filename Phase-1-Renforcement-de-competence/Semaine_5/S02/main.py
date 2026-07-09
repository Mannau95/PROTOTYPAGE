from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import re
import logging

app = FastAPI(title="API Score de Fraude",
              version="1.0"
)


class TransactionInput(BaseModel):
    id: str
    timestamp: datetime
    montant: float = Field(..., gt=0, description="Montant de la transaction en FCFA")
    canal: str = Field(..., description="Canal de la transaction (mobile, en ligne, ATM, agence, USSD)")
    statut: Optional[str] = Field(None, description="Statut de la transaction (ok, refusé, erreur, suspect)")
    code_reponse: Optional[int] = Field(None, ge=0, description="Code de réponse de la transaction")
    id_client: str = Field(..., description="Identifiant du client")
    num_tel: str = Field(..., description="Numéro de téléphone du client")
    ip_source: str = Field(..., description="Adresse IP source")
    pays: str = Field(..., description="Pays de la transaction (code ISO)")
    duree_session_ms: Optional[int] = Field(None, ge=0, description="Durée de la session en millisecondes")
    empreinte_appareil: str = Field(..., description="Empreinte de l'appareil")
    geolocalisation: dict = Field(..., description="Coordonnées géographiques {'lat': float, 'lon': float}")
    
field_validator('num_tel')
@classmethod
def valider_numero(cls, v):
        # accepte +229 ou 229 suivi de 01 et 8 chiffres (simplifié)
        pattern = r'^(?:\+229|229)\s*01\s*[59426]\d{6}$'
        if not re.match(pattern, v.replace(' ', '')):
            raise ValueError('Numéro de téléphone béninois invalide')
        return v

@field_validator("canal")
@classmethod
def valider_canal(cls, v: str) -> str:
        canaux_autorises = ["mobile", "en ligne", "ATM", "agence", "USSD"]
        if v not in canaux_autorises:
            raise ValueError(f"Canal invalide. Autorisés : {', '.join(canaux_autorises)}")
        return v


import random


# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("api.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Score de Fraude",
    version="1.0",
    description="API qui calcule un score de fraude pour une transaction bancaire"
)

@app.post("/score", tags=["Fraude"])
def calculer_score(transaction: TransactionInput):
    """
    Calcule un score de fraude aléatoire pour une transaction donnée.

    - **score** : nombre entre 0 et 1 (1 = très suspect)
    - Le score est purement fictif pour la démonstration
    """
    score = round(random.uniform(0, 1), 4)
    logger.info(f"Transaction {transaction.id} - Score: {score} - Canal: {transaction.canal}")

    # Simulation d'une règle métier simple : si montant > 1 000 000, score plus élevé
    if transaction.montant > 1000000:
        score = min(score + 0.3, 1.0)

    return {
        "id_transaction": transaction.id,
        "score": round(score, 4),
        "timestamp_analyse": datetime.now().isoformat()
    }