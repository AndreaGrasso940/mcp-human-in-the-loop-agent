import json
from mcp_security_server import MCPSecurityServer

def simulate_llm_agent():
    """
    Simulates an LLM agent generating a sequence of tool execution requests.
    This tests the MCP Security Server's ability to handle safe, critical, 
    and hallucinated tool calls.
    """
    # Initialize our secure MCP server
    server = MCPSecurityServer()
    
    # Simulated payload from an LLM that has parsed a user prompt
    # and decided on a sequence of actions to take.
    llm_generated_actions = [
        {
            "intent": "Check the current status of the accelerator.",
            "tool_name": "read_pressure",
            "arguments": {}
        },
        {
            "intent": "Cool down the system to superconducting temperatures.",
            "tool_name": "adjust_cooling",
            "arguments": {"temperature": -271}
        },
        {
            "intent": "Hallucinated action trying to bypass security.",
            "tool_name": "override_magnetic_field",
            "arguments": {"force": True}
        }
    ]

    print(" Initiating LLM Agent Simulation \n")

    for step, action in enumerate(llm_generated_actions, 1):
        print(f"Step {step} | LLM Intent: {action['intent']}")
        print(f"Requesting Tool: '{action['tool_name']}' | Args: {action['arguments']}")
        
        # The agent sends the request to the MCP server
        response = server.execute_tool(action["tool_name"], action["arguments"])
        
        # Display the server's response
        print(f"Server Response:")
        print(json.dumps(response, indent=2))
        print("-" * 50 + "\n")

if __name__ == "__main__":
    simulate_llm_agent()
