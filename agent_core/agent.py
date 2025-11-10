# agent_core/agent.py
from typing import Dict, List, Any , Literal
from llm.base_client import BaseLLMClient
from tools.registry import registry
from prompts.prompts import available_tools_schema

class Agent:
    def __init__(self, llm_client: BaseLLMClient):
        self.llm = llm_client
        self.messages: List[Dict[str, Any]] = []
        self.response_log: List[Dict[str, Any]] = []
        self.available_tools_schema = available_tools_schema

    def set_role(
            self,
            role: Literal["god", "master", "expert", "assistant"] = "assistant",
            ) -> None:
        self.llm.role = role

    def set_mode(
            self,
            mode: Literal["structured_output", "tool_usage"] = "tool_usage",
            ) -> None:
        self.llm.mode = mode

    def add_message(self, role: str, content: Any, source: str = "user") -> None:
        self.messages.append({"role": role, "content": content, "source": source})

    #####################################################

    def ask(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})
        godMode = True
        while godMode:
            response = self.llm.generate_response(messages=self.messages , godMode=godMode , tools_json_schema=self.available_tools_schema)
            self.response_log.append(response)  # Log the response

            # controllo se god ha risolto tutti i sotto-compiti
            error_counter = 0
            for item in response.get("schema", []):
                if item.get("errore"):
                    error_counter += 1
                    # Mando il risultato al modello per continuare
                    self.messages.append({
                        "role": "user",
                        "content": item["errore"],
                        "source": "GOD"
                    })
            if error_counter == 0:
                for item in response.get("schema", []):
                    self.messages.append({
                        "role": "user",
                        "content": item,
                        "source": "GOD"
                    })
                godMode = False

        while True:
            response = self.llm.generate_response(messages=self.messages, tools_json_schema=self.available_tools_schema)
            self.response_log.append(response)  # Log the response
        
            # Caso 1: Risposta finale
            if response["text"]:
                self.messages.append({"role": "model", "content": response["text"] , "source": "llm"})

                # Caso 2: Funzione richiesta
                if response["function_calls"]:
                    if len(response["function_calls"]) == 0:
                        raise ValueError("Nessuna function-call trovata nella risposta del modello.")
                    
                    else:
                        for call in response["function_calls"]:
                            fn = registry.get_function(call["name"])
                            result = fn(**call["arguments"])

                            # Mando il risultato al modello per continuare
                            self.messages.append({
                                "role": "user",
                                "content": str(result),
                                "source": f"function {call['name']}"
                            })

                else:
                    return response["text"]
                

from llm.gemini_client import GeminiLLMClient
from agent import Agent
import tools.math_tools
import tools.conversion_tools
agent = Agent(llm_client=GeminiLLMClient())

response = (agent.ask("dimmi quanto fa 15  piu 3 e poi quanto fa 3 per 2"))