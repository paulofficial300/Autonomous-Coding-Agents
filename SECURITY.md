Critical Security Warning
Running real_agent.py locally gives an AI direct access to your operating system.

The 3 Major Risks:

Prompt Injection: A malicious website the agent visits could secretly command it to read and steal your local passwords or .env files.

Data Destruction: AI hallucinations can result in the agent writing bad scripts that accidentally delete or overwrite important files.

Financial Drain: If the agent gets stuck in an error loop, it will continuously ping the API, rapidly draining your credits.

How to stay safe: Never disable the (y/n) human-in-the-loop approval prompt. Do not let the agent run completely autonomously on your primary computer.
