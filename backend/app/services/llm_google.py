from fastapi import HTTPException, APIRouter
from google import genai
from dotenv import load_dotenv
from classes.agent import agentGemini
import os
from typing import List, Dict , Literal

load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=gemini_api_key)

def ask_gemini(
        prompt: str,
        task: Literal["text" , "streaming_text" , "image" , "video"] = "text"
        ) -> str:
    """Invia un prompt a Gemini e restituisce la risposta come stringa"""
    if task == "text":
        function_call= client.models.generate_content
    if task == "streaming_text":
        function_call= client.models.generate_content_stream
    if task == "image":
        function_call= client.models.generate_images
    if task == "video":
        function_call= client.models.generate_videos

    try:
        response = function_call(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_models() -> List[Dict]:
    """Restituisce la lista dei modelli con name e supported_actions"""
    try:
        models = []
        for model in client.models.list():
            models.append({
                "name": model.name,
                "short_name": model.name.split("/")[-1],
                "display_name": getattr(model, "display_name", ""),
                "description": getattr(model, "description", ""),
                "supported_actions": getattr(model, "supported_actions", [])
            })
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel recupero dei modelli: {str(e)}")

def get_model_names() -> List[str]:
    """Restituisce i nomi dei modelli"""
    models = get_models()
    return set([model["short_name"] for model in models])

def get_actions() -> Dict[str, str]:
    """Restituisce le azioni possibili con descrizioni"""
    actions = set()
    models = get_models()
    for model in models:
        for action in model["supported_actions"]:
            actions.add(action)
    return actions      

def get_actions_for_model(model_name: str) -> List[str]:
    """Restituisce le azioni per un modello specifico"""
    models = get_models()
    for model in models:
        if model["short_name"] == model_name:
            return model["supported_actions"]
    raise HTTPException(status_code=404, detail="Modello non trovato")

def get_models_for_action(action_name: str) -> List[str]:
    """Restituisce i modelli che supportano una azione"""
    models = get_models()
    matching_models = set()
    for model in models:
        if action_name in model["supported_actions"]:
            matching_models.add(model["short_name"])
    if not matching_models:
        raise HTTPException(status_code=404, detail="Azione non supportata da nessun modello")
    return matching_models

agent = agentGemini()
def ask_agent(
        agent : agentGemini,
        question: str
        ) -> Dict[str, str]:
    response = agent.respond_to_question(question)
    if response.function_calls:
        return {"answer" : response.}

# API Router
router = APIRouter(prefix="/gemini" , tags=["Gemini"])

@router.get("/models", response_model=Dict[str , set])
async def api_get_model_names():
    """Restituisce la lista dei nomi dei modelli disponibili"""
    return {"models": get_model_names()}

@router.get("/actions", response_model=Dict[str, set])
async def api_get_actions():
    """Restituisce le possibili azioni con le loro descrizioni"""
    return {"actions": get_actions()}

@router.get("/models/{model_name}/actions", response_model=Dict[str, set])
async def api_get_actions_for_model(model_name: str):
    """Restituisce le azioni disponibili per un modello specifico"""
    return {"actions": get_actions_for_model(model_name)}

@router.get("/actions/{action_name}/models", response_model=Dict[str, set])
async def api_get_models_for_action(action_name: str):
    """Restituisce i modelli che implementano una azione specifica"""
    return {"models": get_models_for_action(action_name)}

