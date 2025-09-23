from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
from langchain_core.runnables import RunnablePassthrough
from Configs import MEMORY_CONFIG, SHOW_INTERMEDIATE_STEPS
from Prompts import create_prompt
from Tools import tools
from Setmodel import llm
from ToolResponse import format_log_message, TEMPLATE_TOOL_RESPONSE
from Parser import JSONOutputParser

def main():
    memory = ConversationBufferMemory(**MEMORY_CONFIG)
    custom_parser = JSONOutputParser()
    prompt = create_prompt(tools)
    agent = (
        RunnablePassthrough.assign(
            agent_scratchpad = lambda x : format_log_message(
                x["input"],
                x["intermediate_steps"],
                template_tool_response = TEMPLATE_TOOL_RESPONSE
            )
        )
        | prompt
        | llm
        | custom_parser
    )
    agent_executor = AgentExecutor(agent = agent, 
                                   tools = tools,
                                   memory = memory, 
                                   return_intermediate_steps = SHOW_INTERMEDIATE_STEPS,
                                   handle_parsing_errors = True,
                                   verbose = True
                                   )
    while True:
        user_input = input("问题：").strip()
        if user_input.lower() in ['exit', 'quit', '退出']:
            print("白白!")
            break
        if user_input.lower() in ['clear', '清除记忆', '清除']:
            memory.clear()
            print("记忆已清除!")
            continue
        if not user_input:
            continue
        try:
            result = agent_executor.invoke({"input": user_input})
            # print(result)
            if SHOW_INTERMEDIATE_STEPS and "intermediate_steps" in result and result["intermediate_steps"]:
                print("\n中间步骤:")
                for i, (action, observation) in enumerate(result["intermediate_steps"], 1):
                    print(f"步骤 {i}:")
                    print(f"动作: {action.tool}")
                    print(f"输入: {action.tool_input}")
                    print(f"输出: {observation}")
                print(f"\n记忆状态: 已记录 {len(memory.chat_memory.messages)} 条消息")
            print("回答：", result["output"])
        except Exception as e:
            print(f"执行错误: {e}")
            
if __name__ == "__main__":
    main()