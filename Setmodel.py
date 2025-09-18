from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model = "deepseek-chat",
    base_url = "https://api.deepseek.com/v1",
    api_key = "sk-490552e0a6e24a9c9a70692b67254983",
    temperature = 0.7
)