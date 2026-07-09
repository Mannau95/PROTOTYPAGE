from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import TransactionInput
import random
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("api.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialisation de l'application
app = FastAPI(
    title="API Score de Fraude",
    version="1.0",
    description="API qui calcule un score de fraude pour une transaction bancaire"
)

# Liste globale pour simuler une base 
transactions_global = []

# Événement au démarrage (optionnel)
@app.on_event("startup")
def startup():
    logger.info("API démarrée avec succès")

# --- Endpoints ---

@app.get("/", tags=["Accueil"], summary="Message d'accueil")
def lire_racine():
    return {"message": "Bienvenue sur l'API de détection de fraude"}

@app.get("/sante", tags=["Administration"], summary="État de l'API")
def sante():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post(
    "/score",
    tags=["Fraude"],
    summary="Calcul de score de fraude",
    description="Reçoit une transaction et retourne un score entre 0 et 1. Plus le score est élevé, plus la transaction est suspecte.",
    response_model=dict
)
def calculer_score(transaction: TransactionInput):
    score = round(random.uniform(0, 1), 4)
    logger.info(f"Transaction {transaction.id} - Score: {score} - Canal: {transaction.canal}")
    
    if transaction.montant > 1000000:
        score = min(score + 0.3, 1.0)
        logger.warning(f"Montant élevé pour la transaction {transaction.id}")
    
    return {
        "id_transaction": transaction.id,
        "score": round(score, 4),
        "timestamp_analyse": datetime.now().isoformat()
    }

# --- Gestionnaires d'erreurs ---

@app.exception_handler(Exception)
def gestion_erreur_globale(request: Request, exc: Exception):
    logger.error(f"Erreur interne : {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Une erreur interne s'est produite."}
    )

@app.exception_handler(RequestValidationError)
def gestion_validation(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation échouée : {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "message": "Données invalides"}
    )