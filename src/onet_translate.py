"""FastMCP server for translating job titles to O*NET occupation codes."""

import logging
from fastmcp import FastMCP
from utils import search_onet_codes_careeronestop_api, search_onet_codes_onet_api

# Configure logging with timestamp
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("onet-translation")


@mcp.tool()
async def search_onet_codes(keyword: str, n_results: int = 3) -> list[dict[str, str]] | dict[str, str]:
    """
    Search for O*NET occupation codes based on a keyword.
    
    Tries CareerOneStop API first, then falls back to O*NET API if no results.
    
    Args:
        keyword: Job title or occupation keyword to search for
        n_results: Number of matching occupations to return (default 3)
    
    Returns:
        List of occupation dicts with 'code' and 'title' keys on success,
        or error dict with 'error' and 'keyword' keys on failure
    """
    # Try CareerOneStop API first
    matching_codes = await search_onet_codes_careeronestop_api(
        keyword=keyword,
        n_results=n_results,
    )
    
    # Fall back to O*NET API if no results
    if not matching_codes:
        logger.info("CareerOneStop returned no results, falling back to O*NET API")
        matching_codes = await search_onet_codes_onet_api(
            keyword=keyword,
            n_results=n_results,
        )
    
    # Return error if both APIs failed
    if not matching_codes:
        error_msg = f"No O*NET codes found for keyword: '{keyword}'"
        logger.error(error_msg)
        return {"error": error_msg, "keyword": keyword}
    
    return matching_codes


def main():
    # Initialize and run the server
    # mcp.run(transport="stdio")
    mcp.run(transport="http", host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()