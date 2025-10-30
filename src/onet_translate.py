from typing import Any
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("onet-translation")

# Constants
API_BASE_URL = "https://api.weather.gov"
USER_AGENT = "careervillage-onet-app/1.0"

async def make_request(url: str) -> dict[str, Any] | None:
    """Make a request to an endpoint with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
def process_data(input_data: str) -> str:
    """Process data on the server"""
    data = make_request(url=API_BASE_URL)
    return f"Processed: {input_data} & {data}"

def main():
    # Initialize and run the server
    mcp.run(transport="http", host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()