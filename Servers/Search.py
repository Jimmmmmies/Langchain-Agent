from mcp.server.fastmcp import FastMCP
from ddgs import DDGS

mcp = FastMCP("Search service", log_level = "ERROR")

@mcp.tool()
def search(query, search_type = "text"):
    """使用DuckDuckGo搜索信息"""
    ddgs = DDGS()
    params = {
        "query" : query,
        "region" : "cn-zh",
        "safesearch" : "off",
        "max_results" : 10,
        "timelimit" : None
    }
    if search_type == "images":
        results = ddgs.images(**params)
    elif search_type == "videos":
        results = ddgs.videos(**params)
    elif search_type == "news":
        results = ddgs.news(**params)
    else:
        results = ddgs.text(**params)
    return results

if __name__ == "__main__":
    mcp.run(transport = "stdio")