from langchain_core.messages import AIMessage, HumanMessage, BaseMessage

TEMPLATE_TOOL_RESPONSE = """
工具响应：
--------------
{observation}
用户的输入：
--------------
请根据刚刚工具的相应，判断是否可以解决用户的问题：
{input}
请根据工具响应的内容，思考接下来的回复。回复格式严格按照prompt中的2中JSON格式，选择其中一种回复。记住回复的格式也必须是JSON格式。
"""

def format_log_message(query, intermediate_steps, template_tool_response):
    thoughts : list[BaseMessage] = []
    for action, observation in intermediate_steps:
        thoughts.append(AIMessage(content=action.log))
        human_message = HumanMessage(
            content = template_tool_response.format(
                input = query,
                observation = observation
            )
        )
        thoughts.append(human_message)
    return thoughts