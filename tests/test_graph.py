from app.graph.builder import build_graph

def test_graph():
    app = build_graph()

    result = app.invoke({
        "input": "What is AI?"
    })
    print(result["output"])
    assert "AI" in result["output"]


