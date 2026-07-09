from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import re


class TransactionInput(BaseModel):
    """
    Modèle de données pour une transaction entrante.
    """

    id: str = Field(
        ...,
        description="Identifiant unique de la transaction",
        example="TXN-12345"
    )

    timestamp: datetime = Field(
        ...,
        description="Date et heure de la transaction (format ISO 8601)",
        example="2026-07-02T14:30:00"
    )

    montant: float = Field(
        ...,
        gt=0,
        description="Montant de la transaction en FCFA (strictement positif)",
        example=15000.50
    )

    canal: str = Field(
        ...,
        description="Canal de la transaction (mobile, en ligne, ATM, agence, USSD)",
        example="mobile"
    )

    statut: Optional[str] = Field(
        None,
        description="Statut de la transaction (ok, refusé, erreur, suspect)",
        example="ok"
    )

    code_reponse: Optional[int] = Field(
        None,
        description="Code de réponse associé au statut",
        example=0
    )

    id_client: str = Field(
        ...,
        description="Identifiant du client",
        example="C-2024-001"
    )

    num_tel: str = Field(
        ...,
        description="Numéro de téléphone au format béninois (+229 01 9X XX XX XX ou 229 01 5X XX XX XX)",
        example="+229 01 97 12 34 56"
    )

    ip_source: str = Field(
        ...,
        description="Adresse IP source de la transaction",
        example="192.168.1.1"
    )

    pays: str = Field(
        ...,
        description="Code pays (ISO) de l'adresse IP",
        example="BJ"
    )

    duree_session_ms: Optional[int] = Field(
        None,
        ge=0,
        description="Durée de la session en millisecondes (>= 0)",
        example=15000
    )

    empreinte_appareil: str = Field(
        ...,
        description="Identifiant de l'appareil (empreinte numérique)",
        example="device_1234"
    )

    geolocalisation: dict = Field(
        ...,
        description="Coordonnées géographiques {lat: float, lon: float}",
        example={"lat": 6.4, "lon": 2.3}
    )

    # --- Validateurs personnalisés (Pydantic V2) ---

    @field_validator("num_tel")
    @classmethod
    def valider_numero(cls, v: str) -> str:
        """
        Valide le format du numéro de téléphone béninois.
        Accepte +229 01 9X XXXXXX ou 229 01 5X XXXXXX (espaces optionnels).
        """
        pattern = r"^(?:\+229|229)\s*01\s*[59]\d{6}$"
        if not re.match(pattern, v.strip()):
            raise ValueError(
                "Format invalide. Utilisez +229 01 9X XX XX XX ou 229 01 5X XX XX XX"
            )
        return v

    @field_validator("canal")
    @classmethod
    def valider_canal(cls, v: str) -> str:
        """Vérifie que le canal est dans la liste autorisée."""
        canaux_autorises = ["mobile", "en ligne", "ATM", "agence", "USSD"]
        if v not in canaux_autorises:
            raise ValueError(
                f"Canal '{v}' invalide. Autorisés : {', '.join(canaux_autorises)}"
            )
        return v

    @field_validator("pays")
    @classmethod
    def valider_pays(cls, v: str) -> str:
        """Vérifie que le pays est un code ISO à 2 lettres (ex: BJ)."""
        if not re.match(r"^[A-Z]{2}$", v):
            raise ValueError("Le code pays doit être en majuscules, ex: BJ")
        return v