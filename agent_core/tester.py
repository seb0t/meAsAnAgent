from llm.gemini_client import GeminiLLMClient
from agent import Agent
import tools.math_tools

agent = Agent(llm_client=GeminiLLMClient())
print(agent.ask("Quanto fa 10 - 3?"))
