from app.graph.builder import build_graph

def run():
    app = build_graph()

    result = app.invoke({
        "input": "Explain LangGraph in simple terms"
    })

    print(result["output"])

if __name__ == "__main__":
    run()

