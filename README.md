# Autonomous-Coding-Agents
This Python script builds an autonomous AI developer using the Google Gemini API. It runs a loop across the four tools: listing files, web search, writing code, and executing scripts. A human-in-the-loop guardrail asks for manual approval before running commands, while an exponential backoff routine gracefully manages the system API rate limits.
