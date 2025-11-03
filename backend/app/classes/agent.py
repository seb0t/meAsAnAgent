from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from typing import List, Dict , Literal 

load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")



class agentGemini:
 

    # Define the function with type hints and docstring
    @staticmethod
    def subtract(a: int, b: int) -> dict:
        """Funzione utile per sottrarre due numeri interi

        Args:
            a: Il primo numero.
            b: Il secondo numero.

        Returns:
            Un dizionario contenente il risultato della sottrazione.
        """
        result = a - b
        return {"result": result}
    
    def _create_function_declaration(self , function : callable) -> Dict:
        """
        Genera automaticamente una dichiarazione (json_schema) di funzione a partire da una funzione Python.
        
        Args:
            function: La funzione Python da cui generare la dichiarazione.
        Returns:
            Una rappresentazione JSON della dichiarazione della funzione.
        """
        return types.FunctionDeclaration.from_callable(
            callable=function,
            client=self.client, 
        ).to_json_dict()
    
    def respond_to_question(self , question : str) -> Dict[str, str]:
        """
        Risponde a una domanda utilizzando il modello Gemini con funzioni abilitate.

        Args:
            question: La domanda posta dall'utente.

        Returns:
            Un dizionario contenente la risposta generata dal modello.
        """

        #TODO: implementare il system prompt
        contents = types.Content(
            role="user",
            parts=[types.Part(text=question)]
        )
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=contents,
            config=self.config,
        )

        if response.tools_responses:
            # Estrarre la risposta dalla funzione chiamata
            tool_response = response.candidates[0].
            return tool_response.output
        return {"answer": response.text}
    
    def __init__(self):

        self.client = genai.Client(api_key=gemini_api_key)
        self.model = "gemini-2.5-flash-lite"  

        # Configure the client

        # Create the function declaration
        subtract_declaration = self._create_function_declaration(
            function=self.subtract
        )

        self.tools = types.Tool(function_declarations=[subtract_declaration])

            # Create the configuration with the function
        self.config = types.GenerateContentConfig(
            tools=[self.tools]
        )

        # Deefine user prompt

        contents = types.Content(
            role="user",
            parts=[types.Part(text="quanto fa 7773-32?")]
        )
        
        # Make the request
        self.response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=self.config,
        )