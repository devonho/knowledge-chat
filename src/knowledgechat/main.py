from stategraph import MyGraph

class Main:
    def main():
        def stream_graph_updates(graph, user_input: str):
            config = {"configurable": {"thread_id": "1"}}
            events = graph.stream({"messages": [{"role": "user", "content": user_input}]}, 
                                  config=config,
                                  stream_mode="values")
            for event in events:
                event["messages"][-1].pretty_print()
                    
                #for value in event.values():
                    # for message in value:
                    #     print(str(type(message)) + ": " + message.content)
                    #print("Assistant:", value["messages"][-1].content)        

        graph = MyGraph.get()
        while True:
            try:
                user_input = input("User: ")
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break

                stream_graph_updates(graph, user_input)
            except:
                # fallback if input() is not available
                user_input = "What do you know about LangGraph?"
                print("User: " + user_input)
                stream_graph_updates(graph, user_input)
                break            

if __name__ == "__main__":
    Main.main()