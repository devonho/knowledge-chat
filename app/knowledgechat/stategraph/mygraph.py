from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt
from langchain_community.tools.tavily_search import TavilySearchResults

from knowledgechat.stategraph.nodes import MyBot, BasicToolNode
from knowledgechat.stategraph.edges import route_tools
from knowledgechat.stategraph import State

from knowledgechat.tools import get_gmail_tools

class MyGraph:
    def get(google_creds_path="./creds/credentials.json"):
        memory = MemorySaver()
        tools=[TavilySearchResults(max_results=2)] + get_gmail_tools(google_creds_path)
        bot_node = MyBot(tools)
        #tool_node = BasicToolNode(tools)
        tool_node = ToolNode(tools=tools)
        
        graph_builder = StateGraph(State)

        # first: the unique node name, 
        # second: the function or object that will be called whenever the node is used.
        graph_builder.add_node("chatbot", bot_node) 
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)
        graph_builder.add_conditional_edges("chatbot", tools_condition)

        graph = graph_builder.compile(checkpointer=memory)

        # with open("graph.png","wb") as f:
        #     f.write(graph.get_graph().draw_mermaid_png())
        return graph