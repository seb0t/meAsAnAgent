# agent_core/tools/registry.py
class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, category="general"):
        def decorator(fn):
            self._tools[fn.__name__] = {
                "fn": fn,
                "category": category,
            }
            return fn
        return decorator

    def get_function(self, name: str):
        return self._tools[name]["fn"]

    def get_tools_schema(self, client) -> list:
        from google.genai import types
        return [
            types.FunctionDeclaration.from_callable(
                callable=data["fn"],
                client=client
            ).to_json_dict()
            for data in self._tools.values()
        ]

registry = ToolRegistry()
