from fastapi import HTTPException, APIRouter
from google import genai
from dotenv import load_dotenv
import os
from typing import List, Dict

load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=gemini_api_key)

# def ask_gemini(prompt: str) -> str:
#     try:
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# collect supported actions from available models (iterate models first, then actions)
try:
	supported_action = set(
		action
		for model in client.models.list()
		for action in getattr(model, "supported_actions", [])
	)
except Exception:
	# fallback to empty set if listing models or accessing attributes fails
	supported_action = set()

# Descriptions for actions
action_descriptions = {
    "generateContent": "Genera contenuto basato su prompt di testo",
    "embedContent": "Crea embeddings vettoriali per il contenuto",
    "countTokens": "Conta i token nel contenuto fornito",
    "chat": "Supporta conversazioni interattive",
    # Add more as needed
}

def get_models() -> List[Dict]:
    """Restituisce la lista dei modelli con name e supported_actions"""
    try:
        models = []
        for model in client.models.list():
            models.append({
                "name": model.name,
                "supported_actions": getattr(model, "supported_actions", [])
            })
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel recupero dei modelli: {str(e)}")

def get_model_names() -> List[str]:
    """Restituisce i nomi dei modelli"""
    models = get_models()
    return [model["name"] for model in models]

def get_actions() -> Dict[str, str]:
    """Restituisce le azioni possibili con descrizioni"""
    actions = {}
    models = get_models()
    for model in models:
        for action in model["supported_actions"]:
            if action not in actions:
                actions[action] = action_descriptions.get(action, f"Azione {action}")
    return actions

def get_actions_for_model(model_name: str) -> List[str]:
    """Restituisce le azioni per un modello specifico"""
    models = get_models()
    for model in models:
        if model["name"] == model_name:
            return model["supported_actions"]
    raise HTTPException(status_code=404, detail="Modello non trovato")

def get_models_for_action(action_name: str) -> List[str]:
    """Restituisce i modelli che supportano una azione"""
    models = get_models()
    matching_models = []
    for model in models:
        if action_name in model["supported_actions"]:
            matching_models.append(model["name"])
    if not matching_models:
        raise HTTPException(status_code=404, detail="Azione non supportata da nessun modello")
    return matching_models

# API Router
router = APIRouter()

@router.get("/models", response_model=List[str])
async def api_get_model_names():
    """Restituisce la lista dei nomi dei modelli disponibili"""
    return get_model_names()

@router.get("/actions", response_model=Dict[str, str])
async def api_get_actions():
    """Restituisce le possibili azioni con le loro descrizioni"""
    return get_actions()

@router.get("/models/{model_name}/actions", response_model=List[str])
async def api_get_actions_for_model(model_name: str):
    """Restituisce le azioni disponibili per un modello specifico"""
    return get_actions_for_model(model_name)

@router.get("/actions/{action_name}/models", response_model=List[str])
async def api_get_models_for_action(action_name: str):
    """Restituisce i modelli che implementano una azione specifica"""
    return get_models_for_action(action_name)

a = get_actions_for_model("models/gemini-2.5-flash")
print("...")