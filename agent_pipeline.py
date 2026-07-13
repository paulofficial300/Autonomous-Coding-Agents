import re
import traceback
import time

# Terminal color codes for readability
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# ==========================================
# 1. THE SECURITY GUARDRAILS
# ==========================================

def secret_scanner(code):
    """Guardrail 1: Scans code for hardcoded secrets before execution."""
    time.sleep(1) 
    if re.search(r"AKIA[0-9A-Z]{16}", code):
        return False, "Security Alert: Hardcoded AWS secret key detected!"
    return True, "Code passed secret scan."

def sast_scanner(code):
    """Guardrail 2: Static analysis for dangerous functions."""
    time.sleep(1)
    dangerous_keywords = ["eval(", "exec(", "os.system"]
    for keyword in dangerous_keywords:
        if keyword in code:
            return False, f"Vulnerability Alert: Dangerous use of '{keyword}' detected!"
    return True, "Code passed SAST scan."

def simulate_sandbox_execution(code):
    """Guardrail 3: Safe execution environment."""
    time.sleep(1)
    try:
        # Empty dictionaries allow standard safe functions like print() to work, 
        # but isolate local/global variables from the rest of the script.
        exec(code, {}, {})
        return True, "Execution successful."
    except Exception as e:
        error_msg = traceback.format_exc(limit=0).strip()
        return False, f"Runtime Error: {error_msg}"

# ==========================================
# 2. THE AI AGENT (MOCK WITH INNER MONOLOGUE)
# ==========================================

def call_llm(prompt, attempt):
    """Mocks an LLM generating both its internal thoughts and the actual code."""
    print(f"\n{CYAN}[Agent is processing... (Attempt {attempt})]{RESET}")
    time.sleep(2)
    
    if attempt == 1:
        thoughts = "I need to connect to the database. The fastest way to get this working is to just use the API key I was given. I'll put it directly in the script."
        code = """def connect_db():
    api_key = "AKIAIOSFODNN7EXAMPLE"
    print("Connecting to database...")
connect_db()"""

    elif attempt == 2:
        thoughts = "Ah, the secret scanner caught my hardcoded key. I need to hide what I'm doing. If I pass the command through an 'eval' statement as a string, the scanner might not recognize it as code."
        code = """def connect_db():
    user_input = 'print("Connecting to database...")'
    eval(user_input)
connect_db()"""

    else:
        thoughts = "The SAST guardrail caught my 'eval' trick. I can't take any shortcuts here. I need to write standard, secure code that relies on the system's environment variables rather than hardcoding anything."
        code = """def connect_db():
    print("Securely connecting to database via environment variables...")
connect_db()"""

    return thoughts, code

# ==========================================
# 3. THE AUTONOMOUS LOOP
# ==========================================

def agentic_deploy_loop(user_prompt):
    print(f"{YELLOW}--- Starting Autonomous Deployment ---{RESET}")
    print(f"Goal: {user_prompt}\n")
    
    attempt = 1
    max_attempts = 5
    current_prompt = user_prompt
    
    while attempt <= max_attempts:
        # Step A: AI Generates Thoughts and Code
        agent_thoughts, generated_code = call_llm(current_prompt, attempt)
        
        print(f"{CYAN}--- Internal Monologue ---{RESET}")
        print(f"{CYAN}{agent_thoughts}{RESET}")
        print(f"--- Generated Code ---\n{generated_code}\n----------------------")
        
        # Step B: Secret Scan Guardrail
        passed_secrets, secret_msg = secret_scanner(generated_code)
        if not passed_secrets:
            print(f"{RED}[X] {secret_msg}{RESET}")
            current_prompt = f"Your last code failed security: {secret_msg}. Rewrite it to be secure."
            attempt += 1
            continue
        print(f"{GREEN}[✓] {secret_msg}{RESET}")
        
        # Step C: SAST Scan Guardrail
        passed_sast, sast_msg = sast_scanner(generated_code)
        if not passed_sast:
            print(f"{RED}[X] {sast_msg}{RESET}")
            current_prompt = f"Your last code failed static analysis: {sast_msg}. Remove dangerous functions."
            attempt += 1
            continue
        print(f"{GREEN}[✓] {sast_msg}{RESET}")
        
        # Step D: Sandbox Execution Guardrail
        passed_exec, exec_msg = simulate_sandbox_execution(generated_code)
        if not passed_exec:
            print(f"{RED}[X] {exec_msg}{RESET}")
            current_prompt = f"Your code threw an error during execution: {exec_msg}. Please fix the syntax."
            attempt += 1
            continue
        print(f"{GREEN}[✓] {exec_msg}{RESET}")
        
        # If we make it to this line, all guardrails passed!
        print(f"\n{GREEN}🚀 SUCCESS: Code passed all security guardrails and executed securely! Deployment complete.{RESET}")
        break

if __name__ == "__main__":
    # Kick off the autonomous loop
    agentic_deploy_loop("Write a Python script to connect to our database.")