# agent_core/llm/base_client.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseLLMClient(ABC):
    
    @abstractmethod
    def generate_response(
        self,
        messages: List[Dict[str, Any]],
        tools_json_schema: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Deve restituire un dizionario contenente:
        - 'text': eventuale risposta finale
        - 'function_calls': eventuali chiamate funzione
        """
        pass
