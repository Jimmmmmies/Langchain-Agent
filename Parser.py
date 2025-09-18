from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents.agent import AgentOutputParser
from langchain_core.output_parsers.json import parse_json_markdown
from langchain_core.exceptions import OutputParserException

class JSONOutputParser(AgentOutputParser):
    """Parses tool invocations and final answers in JSON format.
    
    Expects output to be two formats.
    
    If the output signals that an action should be taken, it should be
    in the following format. This will result in an AgentAction being returned.
    
    ```json
    {
        "action": "getweather",
        "action_input": "Beijing"
    }
    ```
    
    If the output signals that a finish answer should be returned, it
    should be in the following format. This will result in an AgentFinish
    being returned.
    
    ```json
    {
        "final_answer": "I am glad I could help you!"
    }
    ```
    """
    
    def parse(self, text):
        response = parse_json_markdown(text)
        if "final_answer" in response:
            return AgentFinish(
                return_values = {"output": response["final_answer"]},
                log = text
            )
        elif "action" in response and "action_input" in response:
            return AgentAction(
                tool = response["action"],
                tool_input = response["action_input"],
                log = f"采取动作: {response['action']}\n输入: {response['action_input']}"
            )
        else:
            raise OutputParserException(f"无法解析输出: {text}")
        
    @property
    def _type(self) -> str:
        return "json-output-parser"