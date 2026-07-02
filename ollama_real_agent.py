import json
import ollama
from mcp_security_server import MCPSecurityServer

def run_real_agent():
    """
    Connects a local instance of Llama 3.2 to our MCP Security Server.
    The LLM autonomously decides to call a tool based on the user prompt.
    """
    server = MCPSecurityServer()
    
    # 1. Define the tools schema (JSON Schema format expected by LLMs)
    # This tells Llama 3.2 what tools exist and how to use them.
    llm_tools = [
        {
            "type": "function",
            "function": {
                "name": "read_pressure",
                "description": "Reads the current pressure of the accelerator.",
                "parameters": {"type": "object", "properties": {}}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "adjust_cooling",
                "description": "Adjusts the cooling system temperature for the accelerator.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "temperature": {
                            "type": "integer",
                            "description": "The target temperature in Celsius (e.g., -271 for superconducting state)."
                        }
                    },
                    "required": ["temperature"]
                }
            }
        }
    ]

    # 2. Give the AI a scenario
    messages = [
        {
            "role": "system",
            "content": "You are a CERN AI Assistant. Use the provided tools to manage the accelerator."
        },
        {
            "role": "user",
            "content": "Emergency! The accelerator magnets are getting too hot. Cool them down to -271 degrees immediately."
        }
    ]

    print(" Sending prompt to local Llama 3.2 \n")
    
    # 3. Call Ollama with the tools
    response = ollama.chat(
        model='llama3.2',
        messages=messages,
        tools=llm_tools
    )

    # 4. Check if the LLM decided to use a tool
    if response.get("message", {}).get("tool_calls"):
        print("Llama 3.2 decided to take action!\n")
        
        for tool_call in response["message"]["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            tool_args = tool_call["function"]["arguments"]
            
            print(f"LLM is calling Tool: '{tool_name}' with args: {tool_args}")
            
            # 5. Route the real LLM request through our Security Server (Human-in-the-Loop)
            server_response = server.execute_tool(tool_name, tool_args)
            
            print(f"\n Server Final Response:")
            print(json.dumps(server_response, indent=2))
            
    else:
        print("Llama 3.2 just replied with text:")
        print(response["message"]["content"])

if __name__ == "__main__":
    run_real_agent()
