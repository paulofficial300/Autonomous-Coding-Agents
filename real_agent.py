import os
import json
import subprocess
import time
from openai import OpenAI

# Terminal color codes
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Initialize client for Google Gemini
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Using the latest stable model ID
MODEL = "gemini-3.5-flash" 

def write_file(filepath, content):
    with open(filepath, 'w') as f: f.write(content)
    return f"Success: Wrote to {filepath}"

def execute_python(filepath):
    try:
        result = subprocess.run(['python', filepath], capture_output=True, text=True, timeout=10)
        return f"Output:\n{result.stdout}\nErrors:\n{result.stderr}"
    except Exception as e: return str(e)

tools = [
    {"type": "function", "function": {"name": "write_file", "description": "Write code to a file.", "parameters": {"type": "object", "properties": {"filepath": {"type": "string"}, "content": {"type": "string"}}, "required": ["filepath", "content"]}}},
    {"type": "function", "function": {"name": "execute_python", "description": "Run a python script.", "parameters": {"type": "object", "properties": {"filepath": {"type": "string"}}, "required": ["filepath"]}}}
]

def run_agent(goal):
    print(f"{YELLOW}--- Starting Agent (Model: {MODEL}) ---{RESET}")
    
    # Check if model is available first
    try:
        client.models.retrieve(MODEL)
    except:
        print(f"{RED}Model {MODEL} not found. Available models:{RESET}")
        for m in client.models.list().data: print(f" - {m.id}")
        return

    messages = [{"role": "system", "content": "You are an autonomous AI developer. Always explain your thoughts before acting."}, {"role": "user", "content": goal}]
    
    for i in range(5):
        print(f"\n{CYAN}[Agent is thinking... Loop {i+1}]{RESET}")
        try:
            response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
        except Exception as e:
            if "429" in str(e):
                print(f"{RED}Rate limit hit! Waiting 60s...{RESET}")
                time.sleep(60)
                continue
            else:
                print(f"{RED}Error: {e}{RESET}")
                break
        
        msg = response.choices[0].message
        messages.append(msg)
        
        if msg.content: print(f"{CYAN}Thought: {msg.content}{RESET}")
        if msg.tool_calls:
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                if tc.function.name == "write_file": res = write_file(args["filepath"], args["content"])
                else: res = execute_python(args["filepath"])
                print(f"{YELLOW}* Tool {tc.function.name}: {res}{RESET}")
                messages.append({"role": "tool", "tool_call_id": tc.id, "name": tc.function.name, "content": res})
        else: break

if __name__ == "__main__":
    run_agent("Write a python script called 'math_test.py' that calculates the factorial of 5. Save the file, then execute it to prove it works.")
