# CERN Safe AI: MCP Human-in-the-Loop Agent

A lightweight, robust Model Context Protocol (MCP) server implementation designed to mitigate the **"Agentic Loss of Control"** risk in LLM-driven environments.

This project was developed as a practical response to the CERN Computer Security team's concerns regarding autonomous AI agents, ensuring that critical infrastructure operations are protected by strict routing and Human-in-the-Loop (HITL) authorization.

## The Challenge: Agentic Loss of Control
As highlighted in the [CERN Computer Security News: Agentic loss of control (May 2026)](https://home.cern/computer-security-agentic-loss-of-control/), integrating autonomous AI workflows into infrastructure poses severe risks if agents execute unintended or hallucinated commands. The official directive for mitigating these risks is clear: 

> *"Keep tight control of what your agent can access and what it can do. Be precise in the tasks you prompt it to do. Validate the results... Be ready to kill any agent action immediately!"*

## The Solution

This project implements a secure **MCP Server** that exposes tools to an LLM with a Zero-Trust approach:

1. Principle of Least Privilege: Safe, read-only actions (like checking pressure) are executed seamlessly.
2. Human-in-the-Loop (HITL): Critical write actions (like modifying cooling systems) trigger an immediate terminal interrupt (Kill-Switch), requiring explicit human authorization `[Y/N]` before execution.
3. Hallucination Defense: Unauthorized or hallucinated tool calls are automatically blocked and safely handled.

## Project Structure

* `mcp_security_server.py`: The core MCP server defining the tools, routing logic, and the HITL security protocol.
* `ollama_real_agent.py`: An integration script using a local LLM (Llama 3.2 via Ollama) to demonstrate autonomous tool calling and security enforcement.
* `test_mock_agent.py`: A dependency-free simulation script to instantly test the server's routing and security logic without an LLM.

---

## Getting Started

You can test this architecture in two ways: using a real local AI or running a rapid dependency-free mock test.

### Option A: Run with Real AI (Requires Ollama)

This demonstrates a live LLM parsing a natural language emergency, deciding to take action, and being intercepted by the MCP security layer.

Prerequisites:

* Python 3.9+
* Ollama installed and running locally with `llama3.2`.
* `pip install ollama`

Execution:

```bash
python ollama_real_agent.py
```

Live Output:

```text
=== 🧠 Sending prompt to local Llama 3.2 ===

Llama 3.2 decided to take action!

LLM is calling Tool: 'adjust_cooling' with args: {'temperature': '-271'}

[SECURITY ALERT] The AI Agent requests to modify the cooling to -271°C.
Do you authorize this critical operation on the accelerator? [Y/N]: Y

Server Final Response:
{
  "status": "success",
  "message": "Operation authorized. Cooling set to -271°C."
}
```

### Option B: Run Dependency-Free Mock Test

If you want to evaluate the backend logic, routing, and Kill-Switch mechanism instantly without installing AI models, use the mock test.

Execution:

```bash
python test_mock_agent.py
```

## Tech Stack

* Language: Python 3 (Standard Library for core server)
* AI Integration: Ollama API (Llama 3.2)
* Architecture: Model Context Protocol (MCP) pattern, Function Calling
