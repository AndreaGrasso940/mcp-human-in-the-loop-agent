import sys
import json

class MCPSecurityServer:
    """
    Simulated MCP server implementing the Human-in-the-Loop (HITL) protocol 
    for critical actions requested by an AI Agent.
    """
    def __init__(self):
        # Mapping of the tools exposed to the LLM. 
        # Clearly defining which ones are safe and which require human intervention.
        self.tools = {
            "read_pressure": self._read_pressure,
            "adjust_cooling": self._adjust_cooling
        }

    def _read_pressure(self, kwargs):
        """Safe action (Read-only): Returns the current status."""
        # In a real scenario, there would be an API call to the sensors here
        return {
            "status": "success", 
            "pressure_bar": 1.2, 
            "message": "Pressure stable."
        }

    def _adjust_cooling(self, kwargs):
        """Critical action (Write): Requires explicit authorization (HITL)."""
        target_temp = kwargs.get("temperature", 0)
        
        # Print the alert to stderr to separate it from the standard data flow
        print(f"\n[SECURITY ALERT] The AI Agent requests to modify the cooling to {target_temp}°C.", file=sys.stderr)
        
        # The Kill-Switch: Block execution waiting for the human
        user_input = input("Do you authorize this critical operation on the accelerator? [Y/N]: ").strip().upper()
        
        if user_input == 'Y':
            return {
                "status": "success", 
                "message": f"Operation authorized. Cooling set to {target_temp}°C."
            }
        else:
            return {
                "status": "blocked", 
                "error": "Kill-switch activated. Operation cancelled by human operator."
            }

    def execute_tool(self, tool_name, kwargs):
        """Main router that receives requests from the LLM and triggers the tool."""
        if tool_name not in self.tools:
            return {"status": "error", "error": f"Tool '{tool_name}' unauthorized or non-existent."}
        
        # Execution of the requested tool
        return self.tools[tool_name](kwargs)

# LOCAL TEST
if __name__ == "__main__":
    server = MCPSecurityServer()
    
    print("1. Safe Action Test (Read Data) ")
    response_read = server.execute_tool("read_pressure", {})
    print(json.dumps(response_read, indent=2))
    
    print("\n2. Critical Action Test (Agentic Control) ")
    response_write = server.execute_tool("adjust_cooling", {"temperature": -271})
    print(json.dumps(response_write, indent=2))
