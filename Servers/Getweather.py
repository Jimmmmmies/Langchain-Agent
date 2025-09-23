import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather service", log_level = "ERROR")

@mcp.tool()
async def getweather(location: str) -> dict:
    """根据城市获取天气数据"""
    api_key = "SK51HXoMbBdry2-7f"
    url = f"https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={location}&language=zh-Hans&unit=c"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # print(data)
        weather = {
            "city" : data["results"][0]["location"]["name"],
            "description" : data["results"][0]["now"]["text"],
            "temperature" : data["results"][0]["now"]["temperature"]
        }
        return weather
    else:
        raise Exception(f"获取天气失败{response.status_code}")
    
if __name__ == "__main__":
    mcp.run(transport = "stdio")