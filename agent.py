import json
from openai import OpenAI
from config import API_KEY, BASE_URL, MODEL, MAX_STEPS
from prompts import SYSTEM_PROMPT
from schemas import tools
from tools import TOOL_MAP

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

class Agent:
    def __init__(self):
        self.client = client
        self.model = MODEL
        self.tools = tools
        self.tool_map = TOOL_MAP
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def run(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        for _ in range(MAX_STEPS):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto",
            )
            msg = response.choices[0].message
            self.messages.append(msg)

            if not msg.tool_calls:
                print(f"\nAgent: {msg.content}")
                return msg.content

            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                try:
                    args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    args = {}
                print(f"  [tool] {name}({args})")
                func = self.tool_map.get(name)
                result = func(**args) if func else f"Unknown tool: {name}"
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
        print("\nAgent: [max steps reached]")
        return None