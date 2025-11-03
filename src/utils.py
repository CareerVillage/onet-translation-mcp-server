"""Utility functions for fetching O*NET codes from external APIs."""

import logging
import httpx
import settings

logger = logging.getLogger(__name__)


async def search_onet_codes_careeronestop_api(
    keyword: str,
    n_results: int = 3,
    timeout: float = 5.0,
) -> list[dict[str, str]]:
    """
    Search for O*NET codes using CareerOneStop API.
    
    Args:
        keyword: Search term (e.g., "software developer")
        n_results: Number of results to return (default 3)
        timeout: Request timeout in seconds (default 5.0)
    
    Returns:
        List of dicts with 'code' and 'title' keys, or empty list on failure
    """
    logger.info(f"Searching CareerOneStop API for keyword: '{keyword}'")
    
    url = settings.CAREER_ONE_STOP_OCCUPATION_LIST_ENDPOINT.format(
        userId=settings.CAREER_ONE_STOP_WEB_API_USER_ID,
        keyword=keyword,
        dataLevel="N",
        start=0,
        limit=n_results,
    )
    
    headers = {
        "Authorization": f"Bearer {settings.CAREER_ONE_STOP_WEB_API_TOKEN_KEY}",
        "Accept": "application/json"
    }
    
    params = {
        "datasettype": "onet",
        "searchby": "title"
    }
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url=url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
        occupation_list = data.get("OccupationList") or []
        results = []
        for item in occupation_list:
            code = item.get("OnetCode")
            title = item.get("OnetTitle")
            if code and title:
                results.append({"code": code, "title": title})
        
        logger.info(f"CareerOneStop API returned {len(results)} results")
        return results
        
    except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as e:
        logger.warning(f"CareerOneStop API request failed: {e}")
        return []


async def search_onet_codes_onet_api(
    keyword: str,
    n_results: int = 3,
    timeout: float = 5.0
) -> list[dict[str, str]]:
    """
    Fetch O*NET occupation codes from the official O*NET API.
    
    Args:
        keyword: Search term (e.g., "software developer")
        n_results: Number of results to return (max 10, default 3)
        timeout: Request timeout in seconds (default 5.0)
    
    Returns:
        List of dicts with 'code' and 'title' keys, or empty list on failure
    """
    logger.info(f"Searching O*NET API for keyword: '{keyword}'")
    
    headers = {
        "X-API-Key": settings.ONET_API_KEY
    }
    
    params = {
        "keyword": keyword
    }
    
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(settings.ONET_API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        
        occupations = data.get("occupation") or data.get("occupations") or []
        
        if not occupations:
            logger.warning(f"O*NET API returned no occupations for keyword: '{keyword}'")
            return []
        
        results = []
        for occupation in occupations[0:n_results]:
            code = occupation.get("code")
            title = occupation.get("title")
            if code and title:
                results.append({"code": code, "title": title})
        
        logger.info(f"O*NET API returned {len(results)} results")
        return results
        
    except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as e:
        logger.warning(f"O*NET API request failed: {e}")
        return []

