import os
import json
import subprocess
import time
from openai import OpenAI
from duckduckgo_search import DDGS

# --- SETUP ---
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
MODEL = "gemini-2.0-flash"

# --- TOOLS ---
def list_files(): return f"Files: {os.listdir('.')}"
def web_search(query): return json.dumps(list(DDGS().text(query, max_results=2)))
def write_file(filepath, content):
    with open(filepath, 'w') as f: f.write(content)
    return f"Success: Wrote to {filepath}"
def execute_python(filepath):
    res = subprocess.run(['python', filepath], capture_output=True, text=True)
    return f"Stdout: {res.stdout}\nStderr: {res.stderr}"

tools = [
    {"type": "function", "function": {"name": "list_files", "description": "List files in directory."}},
    {"type": "function", "function": {"name": "web_search", "description": "Search web.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "write_file", "description": "Write code.", "parameters": {"type": "object", "properties": {"filepath": {"type": "string"}, "content": {"type": "string"}}, "required": ["filepath", "content"]}}},
    {"type": "function", "function": {"name": "execute_python", "description": "Run script.", "parameters": {"type": "object", "properties": {"filepath": {"type": "string"}}, "required": ["filepath"]}}}
]

# --- AGENT ---
def run_agent(goal):
    messages = [{"role": "system", "content": "You are a developer. Use tools to complete tasks. ALWAYS ask for approval before running a tool."}]
    messages.append({"role": "user", "content": goal})
    
    wait_time = 10
    for _ in range(10):
        try:
            resp = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
            msg = resp.choices[0].message
            messages.append(msg)
            if msg.content: print(f"\nAgent: {msg.content}")
            
            if msg.tool_calls:
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    if input(f"\n[APPROVAL] Run {tc.function.name}({args})? (y/n): ").lower() == 'y':
                        if tc.function.name == "list_files": res = list_files()
                        elif tc.function.name == "web_search": res = web_search(args["query"])
                        elif tc.function.name == "write_file": res = write_file(args["filepath"], args["content"])
                        elif tc.function.name == "execute_python": res = execute_python(args["filepath"])
                        messages.append({"role": "tool", "tool_call_id": tc.id, "name": tc.function.name, "content": str(res)})
                        print(f"Tool Result: {res}")
            else: break
            wait_time = 10 
        except Exception as e:
            if "429" in str(e):
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                wait_time *= 2
            else:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    run_agent("Today is July 13, 2026. List the files in this folder, and create a script 'date_report.py' that prints the current date.")
