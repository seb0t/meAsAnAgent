# agent_core/llm/gemini_client.py
from google import genai
from google.genai import types
from typing import Any, Dict, List ,Literal
from prompts.prompts import SYSTEM_PROMPT , GOD_PROMPT , GodSchema
import os
from dotenv import load_dotenv

from .base_client import BaseLLMClient

load_dotenv()

class GeminiLLMClient(BaseLLMClient):
    
    def __init__(self, 
                 model: str = "gemini-2.5-flash",
                 mode: Literal["structured_output" , "tool_usage"] = "tool_usage",
                 role: Literal["god" , "master" , "expert" , "assistant"] = "assistant",
                 ) -> None:
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = model

        """
        Backbone per la creazione di agenti basati su Gemini.
        Supporta due modalità principali:
        1. tool_usage: per interagire con strumenti esterni tramite function-calls.
        2. structured_output: per generare output strutturati in formato JSON.

        Sono presenti 4 ruoli gerarchicamente ordinati:
        - god: ha il ruolo di supervisore e coordinatore delle attività. scompone i compiti complessi in sotto-compiti più semplici e assegna le funzioni appropriate.
        - master: esperto nella gestione dei compiti, smista le richieste ricevute da god verso gli expert dando loro indicazioni precise su come eseguire i compiti.
        - expert: specialista in domini specifici con conoscenze approfondite, in grado di eseguire tutte le operazioni richieste dai masters.
        - assistant: addetti specializzati alla creazione di contenuti. Gli assistant si occupano di generare risposte testuali chiare e coerenti basate sulle informazioni fornite dagli expert.
        
        #TODO: taggare i tools in base al dominio e in base al ruolo
    
        """

    def generate_response(
        self,
        messages: List[Dict[str, Any]],
        tools_json_schema: List[Dict[str, Any]]| None = None,
        response_json_schema: List[Dict[str, Any]]| None = None,
    ) -> Dict[str, Any]:

        # Converts internal messages into Gemini format
        contents = []
        for message in messages:
            try:
                role = message["role"]
                if message.get("content") and isinstance(message["content"], str):
                    parts = [types.Part(text=message["content"])]
                elif message.get("content") and isinstance(message["content"], types.Blob):
                    parts = [types.Part(inline_data=message["content"])]
                elif message.get("content") and isinstance(message["content"], types.ExecutableCode):
                    parts = [types.Part(executable_code=message["content"])]
                elif message.get("content") and isinstance(message["content"], types.CodeExecutionResult):
                    parts = [types.Part(code_execution_result=message["content"])]
                elif message.get("content") and isinstance(message["content"], types.FunctionCall):
                    parts = [types.Part(function_call=message["content"])]
                elif message.get("content") and isinstance(message["content"], types.FunctionResponse):
                    parts = [types.Part(function_response=message["content"])]

                contents.append(types.Content(role=role, parts=parts))

            except Exception as e:
                raise ValueError(f"Tipo di contenuto non supportato nel messaggio: {message}")


        # caso con tools
        if self.mode == "tool_usage" and tools_json_schema:
            try:
                tools = types.Tool(function_declarations=tools_json_schema)
                config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=[tools],
                    tool_config=types.ToolConfig(
                        function_calling_config=types.FunctionCallingConfig(mode="VALIDATED"),
                    ),
                )
            except Exception as e:
                raise ValueError(f"Errore nella configurazione degli strumenti: {e}")


        # caso con god prompt e json schema
        elif self.mode == "structured_output" and response_json_schema is not None:
            try:
                config = types.GenerateContentConfig(
                    system_instruction=GOD_PROMPT,
                    response_mime_type="application/json",
                    response_json_schema=response_json_schema
                )
            except Exception as e:
                raise ValueError(f"Errore nella configurazione dello schema di risposta: {e}")


        # Genera la risposta dal modello Gemini usando la config corretta
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

        # caso con tools - risponde con testo e function-calls
        if self.mode == "tool_usage" and response.candidates[0].content.parts:
            try:
                output = {}
                for part in response.candidates[0].content.parts:
                    if isinstance(part, str):
                        output["text"] = part
                    elif isinstance(part, types.FunctionCall):
                        output["function_calls"] = [{"name": f"function_{part.name}", "arguments": dict(part.args)}]
                    elif isinstance(part, types.FunctionResponse):
                        output["function_responses"] = [{"name": f"function_{part.name}", "response": part.response}]
                    elif isinstance(part, types.Blob):
                        output["blobs"] = [{"name": "image", "data": part.as_image()}]
                    elif isinstance(part, types.ExecutableCode):
                        output["executable_codes"] = [{"name": "code_snippet", "code": part.code}]
                    elif isinstance(part, types.CodeExecutionResult):
                        output["code_execution_results"] = [{"name": "executed_code", "result": part.outcome}]
            except Exception as e:
                raise ValueError(f"Errore nell'estrazione della risposta: {e}")     

        elif self.mode == "structured_output" and response.candidates[0].content.parts:
            try:
                return response.parsed
            except Exception as e:
                raise ValueError(f"Errore nel parsing della risposta strutturata: {e}")
            
            
            
            
            
            
        #     text_parts = ""
        #     function_calls = []

        #     parts_list = response.candidates[0].content.parts
        #     for part in parts_list:
        #         if part.text:
        #             text_parts += part.text
        #         if part.function_call:
        #             function_calls.append(part.function_call)

        #     output = {"text": text_parts, "function_calls": []}

        #     if function_calls:
        #         for fc in function_calls:
        #             output["function_calls"].append({
        #                 "name": fc.name,
        #                 "arguments": dict(fc.args)
        #             })

        #     return output
        
        # # caso GOD prompt - risponde sempre con json strutturato

        # elif godMode:

        #     god_prompt_response = response.parsed
        #     return god_prompt_response
