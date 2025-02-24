from langchain_anthropic import ChatAnthropic
from stategraph import State

class MyBot:
    def __init__(self, tools: list):
        self.llm = ChatAnthropic(model="claude-3-5-sonnet-20240620").bind_tools(tools)

    def __call__(self, state: State):
        return {"messages": [self.llm.invoke(state["messages"])]}
