from langgraph.graph import StateGraph, START, END
from langchain_community.tools.tavily_search import TavilySearchResults
from stategraph.nodes import MyBot, BasicToolNode
from stategraph import State

class MyGraph:
    def get():
        tools=[TavilySearchResults(max_results=2)]
        bot_node = MyBot(tools)
        tool_node = BasicToolNode(tools)
        
        graph_builder = StateGraph(State)

        # first: the unique node name, 
        # second: the function or object that will be called whenever the node is used.
        graph_builder.add_node("chatbot", bot_node) 
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)

        graph = graph_builder.compile()

        # with open("graph.png","wb") as f:
        #     f.write(graph.get_graph().draw_mermaid_png())
        return graph